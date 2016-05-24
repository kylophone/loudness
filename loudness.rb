require 'open3'
require 'json'

ffmpeg_bin = "/usr/local/bin/ffmpeg"
target_il  = -24.0 
target_lra = +11.0
target_tp  = -2.0
samplerate = "48k"

if ARGF.argv.count != 2
  puts "Usage: #{$0} input.wav output.wav"
  exit -1
end

ff_string  = "#{ffmpeg_bin} -hide_banner "
ff_string += "-i #{ARGF.argv[0]} "
ff_string += "-af loudnorm=I=#{target_il}:LRA=#{target_lra}:tp=#{target_tp}:print_format=json "
ff_string += "-f null -"

stdin, stdout, stderr, wait_thr = Open3.popen3(ff_string)

if wait_thr.value.success?
  stats = JSON.parse(stderr.read.lines[-12,12].join)
  loudnorm_string  = "-af loudnorm=print_format=summary:linear=true:I=#{target_il}:LRA=#{target_lra}:tp=#{target_tp}"
  loudnorm_string += ":measured_I=#{stats["input_i"]}:measured_LRA=#{stats["input_lra"]}:measured_tp=#{stats["input_tp"]}:measured_thresh=#{stats["input_thresh"]}:offset=#{stats["target_offset"]}"
else
  puts stderr.read
  exit -1
end

ff_string  = "#{ffmpeg_bin} -y -hide_banner "
ff_string += "-i #{ARGF.argv[0]} "
ff_string += "#{loudnorm_string} "
ff_string += "-ar #{samplerate} "
ff_string += "#{ARGF.argv[1]}"

stdin, stdout, stderr, wait_thr = Open3.popen3(ff_string)

if wait_thr.value.success?
  puts stderr.read.lines[-12,12].join
  exit 0
else
  puts stderr.read
  exit -1
end
