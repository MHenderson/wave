env = Environment()

prefix = '/home/matthew/Working/Wave'

suffices = ['']

inputs = [prefix + suffix for suffix in suffices]
string_inputs = ''
for input in inputs:
    string_inputs += (input + ':')

env['TEXINPUTS'] = ':.:/home/matthew/.TeX:' + string_inputs
env['PDFLATEXCOM'] = 'cd ${TARGET.dir} && export TEXINPUTS=$TEXINPUTS && $PDFLATEX --shell-escape $PDFLATEXFLAGS ${SOURCE.file}'
Export('env')

SConscript(['SConscript'],build_dir='/home/matthew/Documents/Wave')
