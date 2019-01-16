# Model Artitecture Planning

### Membership
- slug
- type (free, pro, enterprise)
- price
- stripe plan id


### UserMembership
- User  (Foreign Key Membership)
- Stripe Customer Id
- Membership type   (Foreign Key Membership)

### Subscription
- User Membership
- stripe subscription id
- active    (Foreign Key to UserMembership)

### Course
- slug
- title
- description
- allowed memberships (Foreign Key to Membership)
### Lesson
- slug
- title
- Course    (Foreign Key to Course)
- position
- video
- thumbnail