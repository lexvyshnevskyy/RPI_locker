Place it in /etc/systemd/system folder with a name like lock.service.

Make sure that your script is executable with:

    chmod u+x /home/pi/LockApp/run.py
Start it:

    sudo systemctl start lock.service
Enable it to run at boot:

    sudo systemctl enable lock.service
Stop it:
    
    sudo systemctl stop lock.service

mqtt topics and responses
mobile application publish to topic `Lock/status`  json string:

    {"lock":1,"is_opened":true}
where
Lock: integer, number of lock 0-1-2
Is_opened: bool, True -> open

Lock publish to next topic `Lock/response` json string:

        {
        "code": 500,
        "message": "list index out of range"
        }
Where
code: integer 500 some error happen
message: string, error description

    {
      "code": 200,
      "message": "Ok"
    }
Where
code: integer 200 ok
Message: string "Ok"

Shadow
Every 0.5 seconds Lock publish to topic `shadow/status` status of system, like pin-pong

    {
      "code": 200,
      "message": "False"
    }
Where
code: integer 200 ok
Message: bool true->lock is opened, false->lock is closed.
This show 3 channels in one message

hardware

https://diylab.com.ua/p678100820-raspberry-model-ghz.html

https://diylab.com.ua/p516034608-rele-plata-rozshirennya.html