# CENG495-HW1 

MongoDB flask application

## Run Locally

Create venv

```bash
  python3 -m venv venv
```

Activate venv

```bash
  source venv/bin/activate
```

Deactivate venv

```bash
  deactivate
```

Starting MongoDb

```bash
  sudo systemctl start mongod
```

Stopping MongoDb

```bash
  sudo systemctl stop mongod
```

## Vercel URL

[Click Here](https://ceng-495-hw-1.vercel.app)


## 🚀 About Project

You can login as the following users.

1) Admin User: username: admin -  password: 1982%admin 
2) test Users: test(integer from 0 to 9) - password: test



### Example users: 
    test0:test
    test1:test
    and so on..

I have chosen **Python** because It is the language I have used mostly in my internship, part time and academic career along with C and C++. I already had very limited Django and Flask experience. Thus, I decidede to move on with Flask considering that **PyMongo** is useful for **MongoDB**. 


I think the website is very user friendly. 

- The **log in/out** button is located in the right-upper corner. After login process, the authorization distinction between test users and the admin is visible. **Admin Panel** is only reachable from admin accounts.
- **Item/User addittion/deletion** is available from admin panel
- **Categorization & search** functionalities work well from **navbar**
- **My Profile** part is for seeing some statistics related to the user
- **Item Details** are visible for only authorized users and located in a different tab that can be reached from **details** button.
- After clickin the **details** button, one can see the interface for **review & rate**. Also, reviews by others can bee seen as well as the average rate.
- Passwords are not stored, their hashes are stored on db. **werkzeug.security** have been used in Python for this purpose.
- There is no hardcoded credentials on the code. I recieve them as **environment variables**.
