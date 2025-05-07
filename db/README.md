# COMMANDS DB description

## one command contains:
-   command
-   status
-   command_id
-   tstamp

### command may contain one out of following strings:
```["toggle_machine","","","","","",""]```

### status may contain one out of following strings:
```["pending","failed","served","rejected"]```

### command_id is a random generated 4 chars long integer to identify the exact command between Server frontend Database and ESP

### tstamp is the exact Date at the first ever creation of the db entry and does not say anything about completion or rejection.

## NOTE:
### A created command is marked as failed after 5 minutes if its status is still pending, to ensure that no processes continue after a communication failure in the chain.