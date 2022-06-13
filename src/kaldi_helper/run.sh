#!/usr/bin/env bash

audio_file=`realpath "$1"`
tmp=`realpath "$2"`

cd src/kaldi_helper

. ./cmd.sh
. ./path.sh

NAME=$(basename "$audio_file")
NAME=$(echo "${NAME%.*}" | tr '[:upper:]' '[:lower:]' | sed -e 's/ /_/g')
echo $NAME
EXT="${audio_file##*.}"

data=$tmp/data
tmp_audio_dir=$tmp/audios
logs=$tmp/logs
decode_results=$tmp/decode_results

mkdir -p "$data"
mkdir -p "$tmp_audio_dir"
mkdir -p "$logs"
mkdir -p "$decode_results"

# Converse to wav if need then Create segment 10s
ffmpeg -i "$audio_file" -acodec pcm_s16le -ac 1 -ar 16000 "$tmp/$NAME.wav"
ffmpeg -i "$tmp/$NAME.wav" -f segment -segment_time 10 -c copy "$tmp_audio_dir/$NAME-%03d.wav"

# Create esential kaldi data format
python3 local/prepare_data.py "$tmp_audio_dir" $data
utils/fix_data_dir.sh $data

# Make mfcc and normalize mfcc feature
steps/make_mfcc.sh --cmd "$train_cmd" --nj 16 --mfcc-config \
conf/mfcc_hires.conf $data $logs/make_mfcc $mfcc

steps/compute_cmvn_stats.sh $data $logs/make_mfcc $mfcc

# Extract ivector feature
nspk=$(wc -l <$data/spk2utt)
steps/online/nnet2/extract_ivectors_online.sh --cmd "$train_cmd" --nj "$nspk" \
$data exp/nnet3_cleaned/extractor $data/ivectors

dir=exp/chain_cleaned/tdnn_1d_sp
graph_dir=$dir/graph_tgsmall

# # Create the lmgraph
# utils/mkgraph.sh --self-loop-scale 1.0 --remove-oov \
#   data/lang_test_tgsmall $dir $graph_dir

# Decode
steps/nnet3/decode.sh --acwt 1.0 --post-decode-acwt 10.0 \
    --nj $nspk --cmd "$decode_cmd" \
    --online-ivector-dir $data/ivectors \
    $graph_dir $data $decode_results

# Score decode result
steps/score_kaldi.sh --cmd "run.pl" $data $graph_dir $decode_results
# cat exp/chain_cleaned/tdnn_1d_sp/decode_test_tgsmall/scoring_kaldi/best_wer

cd ../..