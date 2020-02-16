```text
NOT RUN
```
<br>        
    

```Python3

@app.route('/attachremote', methods=['GET', 'POST'])
def addremote():
    try:
        shell('usbip attach -r  ' + str(request.remote_addr) + ' -b 1-1.2')
    except:
        print('could not attach.  continuing...')
    return render_template('server_home.jade',
                           server_addr=self_addr,
                           your_addr=str(request.remote_addr),
                           is_enabled=str(ip_conf_dict.__contains__(request.remote_addr)))


```  
