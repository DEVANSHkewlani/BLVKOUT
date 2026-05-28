def extract_user_data(user):

    return {
        "id": user.id,
        "email": user.email,
        "role": user.user_metadata.get(
            "role",
            "user"
        )
    }