import re

single_comment = re.compile("//")
multi_comment_start = re.compile("r/\*\*")
multi_comment_end = re.compile("r$\*/")


