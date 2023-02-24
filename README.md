# SimplePomodoro
This is a very simple to use pomodoro timer for the cli. It's superpower is to be very flexible in bringing you through the whole office workday by considering that not every session can be finished well and that you have to attend meetings.

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

### Meeting sessions
In office life, meetings are like the weird friend at a party: No one enjoys it to be there but without it also wouldn't work out. To keep track with doing enough break I implemented a command to track meeting time and calculate the break time you deserved afterwards:
```
sp meet
```
This command will start a stopwatch, which tells you the current time spent in the meeting. You can end the meeting timer by pressing `CTRL-C`.

By using
```
sp meet [minutes] 
```
you can let SimplePomodoro calculate the deserved break duration after a meeting of x minutes. This can be helpful when you forget to start the stopwatch.

### Cofiguration
You can change the configuration by using
```
sipo config
```

