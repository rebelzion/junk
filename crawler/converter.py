import os
from typing import List, Optional


class Converter:


    def __init__(self,ffmpeg_binary: str):
        self.ffmpeg_binary = ffmpeg_binary



    def check_is_corrupted(self, video: str) -> bool:
        pass



    def _get_params(self, src_format: str, output_format: str) -> List[str]:

        if src_format == "m3u8" and output_format == "mp4":
            return ["-bsf:a","aac_adtstoasc","-vcodec","copy","-c","copy","-crf","50"]

    def convert(self, input_file: str, output_format: str, output: str) -> bool:

        # determine parameters for ffmpeg conversion
        src_format = input_file.rstrip(".",1)[-1]
        params = self._get_params(src_format, output_format)

        if os.path.isdir(output):
            basename = input_file.split("/")[-1]
            stem, ext = basename.rsplit(".", 1)
            output_file = os.path.join(output, f"{stem}.{output_format}")
        else:
            output_file = output

        # assemble all parameters
        params = [self.ffmpeg_binary, "-i", input_file] + params + [output_file]

        # try to convert
        try:
            if subprocess.run(params).returncode == 0:
                if not self.check_is_corrupted(output_file):
                    print(f"Successfully converted {input_file=} to {output_file=}")
                    return True
                else:
                    print(f"Removing corrupted {output_file=}")
                    os.remove(output_file)
                    return False
        except Exception as e:
            print(f"Could not convert {input_file=}: {e=}")
            return False
