#!/usr/bin/env ruby

require 'open3'
require 'json'

ffmpeg_bin = '/usr/local/bin/ffmpeg'
target_il  = -24.0
target_lra = +11.0
target_tp  = -2.0
samplerate = '48k'

if ARGF.argv.count != 2
  puts "Usage: #{$PROGRAM_NAME} input.wav output.wav"
  exit 1
end

ff_string  = "#{ffmpeg_bin} -hide_banner "
ff_string += "-i #{ARGF.argv[0]} "
ff_string += '-af loudnorm='
ff_string += 'dual_mono=true:'
ff_string += "I=#{target_il}:"
ff_string += "LRA=#{target_lra}:"
ff_string += "tp=#{target_tp}:"
ff_string += 'print_format=json '
ff_string += '-f null -'

_stdin, _stdout, stderr, wait_thr = Open3.popen3(ff_string)

if wait_thr.value.success?
  stats = JSON.parse(stderr.read.lines[-12, 12].join)
  loudnorm_string  = '-af loudnorm='
  loudnorm_string += 'dual_mono=true:'
  loudnorm_string += 'print_format=summary:'
  loudnorm_string += 'linear=true:'
  loudnorm_string += "I=#{target_il}:"
  loudnorm_string += "LRA=#{target_lra}:"
  loudnorm_string += "tp=#{target_tp}:"
  loudnorm_string += "measured_I=#{stats['input_i']}:"
  loudnorm_string += "measured_LRA=#{stats['input_lra']}:"
  loudnorm_string += "measured_tp=#{stats['input_tp']}:"
  loudnorm_string += "measured_thresh=#{stats['input_thresh']}:"
  loudnorm_string += "offset=#{stats['target_offset']}"
else
  puts stderr.read
  exit 1
end

ff_string  = "#{ffmpeg_bin} -y -hide_banner "
ff_string += "-i #{ARGF.argv[0]} "
ff_string += "#{loudnorm_string} "
ff_string += "-ar #{samplerate} "
ff_string += ARGF.argv[1].to_s

_stdin, _stdout, stderr, wait_thr = Open3.popen3(ff_string)

if wait_thr.value.success?
  puts stderr.read.lines[-12, 12].join
  exit 0
else
  puts stderr.read
  exit 1
end
