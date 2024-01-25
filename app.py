from ai.post_recommender import PostRecommender
import streamlit as st


def main():
    st.title("Post Recommender")
    st.subheader("This is a post recommender system based on generative AI")

    # take input username
    username = st.text_input("Enter your username")
    # take input 2
    posts = st.text_input("Enter the posts you like")

    if st.button("Get Tags"):
        # create an instance of the PostRecommender class
        with st.spinner("Loading AI model"):
            post_recommender = PostRecommender(tags_txt_path="./ai/tags.txt")

            # get the user tags
            user_tags = post_recommender.get_user_tags(username, posts)

        # display the user tags
        st.subheader("User Tags")
        st.write(user_tags)


if __name__ == "__main__":
    main()
