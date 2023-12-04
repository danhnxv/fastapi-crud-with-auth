mongosh -- "$MONGODB_DATABASE" <<EOF
    var rootUser = '$MONGO_INITDB_ROOT_USERNAME';
    var rootPassword = '$MONGO_INITDB_ROOT_PASSWORD';
    var admin = db.getSiblingDB('admin');
    admin.auth(rootUser, rootPassword);

    var user = '$MONGODB_USERNAME';
    var passwd = '$MONGODB_PASSWORD';

    db.createUser({user: user, pwd: passwd, roles: ["readWrite", "dbAdmin"]});
    use $MONGODB_DATABASE;
    db.auth(user, passwd);
    db.Users.insertOne({
        "_cls": "User",
        "username": "fastapi",
        "fullname": "FastAPI",
        "role": "admin",
        "hashed_password": "\$2b$12$6EeTX9vx4kQ9uIwL5tEDK.5j.F65zMS7kDNtLgHMcvd9RPkGgjGQO",
        "created_at": new Date(),
        "updated_at": new Date(),
    });
EOF
