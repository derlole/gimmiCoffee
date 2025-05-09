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


# COFFEE DB description

## one command contains:
-   user
-   status
-   tstamp

### user may contain a string about the user that started the coffee making process

### status may contain one out of following strings:
```["pending","failed","served","rejected"]```

## NOTE
### A Coffee making process is going through a command creation in the backend, therefore a coffee status can be rejected by the esp or fail after 5 minutes. If the according command fails the coffee fails.