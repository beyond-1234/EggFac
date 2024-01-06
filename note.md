## stream selection

### automatic stream selection

In the absence of any map options for a particular output file, ffmpeg inspects the output format to check which type of streams can be included in it, viz. video, audio and/or subtitles. For each acceptable stream type, ffmpeg will pick one stream, when available, from among all the inputs.

- It will select that stream based upon the following criteria:
 - for video, it is the stream with the highest resolution,
 - for audio, it is the stream with the most channels,
 - for subtitles, it is the first subtitle stream found but there’s a caveat.
  -  `The output format’s default subtitle encoder can be either text-based or image-based, and only a subtitle stream of the same type will be chosen.`
 - In the case where several streams of the same type rate equally, the stream with the lowest index is chosen.

Data or attachment streams are not automatically selected and can only be included using -map.

### Stream specifiers

A stream specifier is a string generally appended to the option name and separated from it by a colon. E.g. -codec:a:1 ac3 contains the a:1 stream specifier, which matches the second audio stream. Therefore, it would select the ac3 codec for the second audio stream.

A stream specifier can match several streams, so that the option is applied to all of them. E.g. the stream specifier in -b:a 128k matches all audio streams.

An empty stream specifier matches all streams. For example, -codec copy or -codec: copy would copy all the streams without reencoding.

- stream_type
 - stream_type is one of following: ’v’ or ’V’ for video, ’a’ for audio, ’s’ for subtitle, ’d’ for data, and ’t’ for attachments.
 - ’v’ matches all video streams, ’V’ only matches video streams which are not attached pictures, video thumbnails or cover arts.
 - additional_stream_specifier is not discussed here

### Generic options

By default the program logs to stderr. If coloring is supported by the terminal, colors are used to mark errors and warnings. Log coloring can be disabled setting the environment variable AV_LOG_FORCE_NOCOLOR, or can be forced setting the environment variable AV_LOG_FORCE_COLOR.
