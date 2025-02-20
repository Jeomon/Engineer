from subprocess import run, PIPE,Popen
from termcolor import colored

app_name = 'tic_tac_toe'
process=Popen(['python',f'./{app_name}/main.py'],text=True,stderr=PIPE,stdout=PIPE)

while True:
    try:
        output=process.stdout.read()
        print(output)
        error=process.stderr.read()
        print(error)
        if process.poll() is not None:
            break
    except KeyboardInterrupt:
        print('App stopped by the user')
        process.terminate()
        break
