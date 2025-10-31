# Authentication System Documentation

The auth system is currently using a JWT Token implementation.
Inside the DB only the hashed_password is stored.

To verify login access we're using the token on login to see if the user has a valid token.
If not then he'll be restricted from accessing routes that are strictly usable for logged in users.

- Algorithm + JWT-Key for high security level.


# User Management

As of now, there are only 3 types of users.
User | Admin | Superuser

All API routes must be secured to only allow the concerned user group(s).

For example, only Admin & Superuser are allowed to delete users.
( This should be reviewed as another type of restriction such as "restricted account", "blacklisted account" or even 
"disabled account" ).