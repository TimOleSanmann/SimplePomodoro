# SimplePomodoro
This is a very simple to use pomodoro timer for the cli. 
## Usage
### Work sessions
Starting a work session:
``` 
sipo work [minutes]
```
Starting a worksession without adding a number, the duration is read from the config file. The default value for it is 50 minutes. Worksessions can be interupted by pressing `CTRL-C`.

### Break sessions
Starting a break session:
```
sipo break [minutes]
```
Like with the work session, you can add a custom duration to the break session. By default it is 10 minutes, which is also read from the config file. Break sessions can be interupted by pressing `CTRL-C`.


### Cofiguration
You can change the configuration by using
```
sipo config
```

