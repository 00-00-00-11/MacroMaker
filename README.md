# MacroMaker
Easy to use macro software for Windows that works with .txt files to function.

## Download
You can find all releases [here](https://github.com/AlexFlipnote/MacroMaker/releases).<br>
If Windows Defender comes up and warns you, the only reason it does such is due to unsigned software. (Not paying for that..)

## How to use
Simply make a .txt file at the same file location as the MacroMaker.exe and it will see the "script".
Making it work with what you desire is not hard at all, here are the different things you can do:

#### Write something
```
WRITE The quick brown fox jumps over the lazy dog.
WRITE dead meme xd
```

#### Press key(s)
```
PRESS c
PRESS ctrl+a
PRESS ctrl+alt+del
```

#### Timeout
The numbers are defined as seconds, if you want (example) 500 milliseconds, you need to do `0.5`.
```
TIMEOUT 2
TIMEOUT 0.5
TIMEOUT 100
```

#### Debug mode
Useful if you want to see if MacroMaker is doing everything you want it to do (it can be spammy).
Remember to have it on top of the entire script, easier to sort at least.
```
DEBUG TRUE
```


## Discord
If you want to visit my Discord: https://discord.gg/DpxkY3x

## Sources
- [boppreh/keyboard](https://github.com/boppreh/keyboard) (Will use later for easier escape of macro)
- [ethanhs/pyhooked](https://github.com/ethanhs/pyhooked)
