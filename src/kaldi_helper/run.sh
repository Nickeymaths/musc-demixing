#!/usr/bin/env bash

audio_file=`realpath "$1"`
tmp=`realpath "$2"`
logdir=`realpath "$3"`

cd src/kaldi_helper

. ./cmd.sh
. ./path.sh

NAME=$(basename "$audio_file")
NAME=$(echo "${NAME%.*}" | tr '[:upper:]' '[:lower:]' | sed -e 's/ /_/g')
EXT="${audio_file##*.}"

# prepare output, log directories
mkdir -p "$tmp/$NAME"
mkdir -p "$logdir/$NAME"
tmp="$tmp/$NAME"
logdir="$logdir/$NAME"

data=$tmp/data
tmp_audio_dir=$tmp/audios
decode_results=$tmp/decode_results

mkdir -p "$data"
mkdir -p "$tmp_audio_dir"
mkdir -p "$decode_results"

# Converse to wav if need then Create segment 10s
ffmpeg -i "$audio_file" -acodec pcm_s16le -ac 1 -ar 16000 "$tmp/$NAME.wav"
ffmpeg -i "$tmp/$NAME.wav" -f segment -segment_time 10 -c copy "$tmp_audio_dir/$NAME-%03d.wav"

# Create esential kaldi data format
python3 local/prepare_data.py "$tmp_audio_dir" $data
utils/fix_data_dir.sh $data

# Make mfcc and normalize mfcc feature
steps/make_mfcc.sh --cmd "$train_cmd" --nj 16 --mfcc-config \
conf/mfcc_hires.conf $data $data/log/make_mfcc $mfcc

steps/compute_cmvn_stats.sh $data $data/log/make_mfcc $mfcc

# Extract ivector feature
nspk=$(wc -l <$data/spk2utt)
steps/online/nnet2/extract_ivectors_online.sh --cmd "$train_cmd" --nj "$nspk" \
$data exp/nnet3_cleaned/extractor $data/ivectors

dir=exp/chain_cleaned/tdnn_1d_sp
graph_dir=$dir/graph_tgsmall

# # Create the lmgraph
# utils/mkgraph.sh --self-loop-scale 1.0 --remove-oov \
#   local/lang_test_tgsmall $dir $graph_dir

# Decode
steps/nnet3/decode.sh --acwt 1.0 --post-decode-acwt 10.0 \
    --nj $nspk --cmd "$decode_cmd" \
    --online-ivector-dir $data/ivectors \
    $graph_dir $data $decode_results

# Score decode result
steps/score_kaldi.sh --cmd "run.pl" $data $graph_dir $decode_results
# cat exp/chain_cleaned/tdnn_1d_sp/decode_test_tgsmall/scoring_kaldi/best_wer

# Move log dir from default kaldi log to user log directories
mkdir -p "$logdir/ivectors"
mv "$data/ivectors/log/"* "$logdir/ivectors"

mkdir -p "$logdir/make_mfcc"
mv "$data/log/make_mfcc/"* "$logdir/make_mfcc"

mkdir -p "$logdir/decode"
mv "$decode_results/log/"* "$logdir/decode"

mkdir -p "$logdir/score"
mv "$decode_results/scoring_kaldi/log/"* "$logdir/score"

# Remove tmpdir
rm -r "$tmp"

cd ../..