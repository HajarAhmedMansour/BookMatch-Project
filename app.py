import os
import streamlit as st
import requests
from dotenv import load_dotenv

# --------------------------------------------------
# Configuration
# --------------------------------------------------

load_dotenv()

API_URL = os.getenv("BOOKMATCH_API_URL", "").rstrip("/")

if not API_URL:
    st.error(
        "Backend URL is missing. "
        "Please configure BOOKMATCH_API_URL in your .env file."
    )
    st.stop()


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="BookMatch",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# Custom styling
# --------------------------------------------------

st.markdown(
    """
    <style>

    .main {
        padding-top: 2rem;
    }

    .book-card {
        padding: 1.2rem;
        border-radius: 12px;
        border: 1px solid #dddddd;
        margin-bottom: 1.5rem;
        background-color: #ffffff;
    }

    .book-title {
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }

    .book-author {
        font-size: 1rem;
        color: #666666;
        margin-bottom: 0.8rem;
    }

    .explanation {
        line-height: 1.6;
        margin-top: 0.8rem;
    }

    .similarity {
        font-size: 0.9rem;
        color: #777777;
        margin-top: 0.5rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("BookMatch")

st.markdown(
    """
    ### Find your next book

    Describe what you are in the mood for, mention a book
    you already like, or combine both.
    """
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("Recommendation settings")

    top_k = st.slider(
        "Number of recommendations",
        min_value=3,
        max_value=10,
        value=5
    )

    st.markdown("---")

    st.markdown(
        """
        **Examples**

        * A dark mystery with suspense

        * Something like The Alchemist,
          but with a different author

        * An emotional historical novel

        * Recommend something emotional but not too long
        """
    )


# --------------------------------------------------
# User query
# --------------------------------------------------

query = st.text_area(
    "What would you like to read?",
    placeholder=(
        "Example: I'm reading The Alchemist and "
        "want something similar but less fantasy."
    ),
    height=120
)


# --------------------------------------------------
# Recommendation button
# --------------------------------------------------

recommend_button = st.button(
    "Find books",
    type="primary",
    use_container_width=True
)


# --------------------------------------------------
# Recommendation request
# --------------------------------------------------

if recommend_button:

    if not query.strip():

        st.warning(
            "Please describe what you would like to read."
        )

    else:

        with st.spinner(
            "Finding books that match your request..."
        ):

            try:

                response = requests.post(
                    f"{API_URL}/recommend",
                    json={
                        "query": query,
                        "top_k": top_k
                    },
                    timeout=180
                )

                response.raise_for_status()

                data = response.json()

            except requests.exceptions.Timeout:

                st.error(
                    "The recommendation service took too long "
                    "to respond. Please try again."
                )

                st.stop()

            except requests.exceptions.RequestException as error:

                st.error(
                    "Could not connect to the BookMatch backend."
                )

                st.code(str(error))

                st.stop()


        # --------------------------------------------------
        # Backend error
        # --------------------------------------------------

        if not data.get("success", False):

            st.error(
                data.get(
                    "message",
                    "Unable to generate recommendations."
                )
            )

            st.stop()


        # --------------------------------------------------
        # Parsed request
        # --------------------------------------------------

        parsed = data.get(
            "parsed_query",
            {}
        )

        reference_book = data.get(
            "reference_book"
        )

        recommendations = data.get(
            "recommendations",
            []
        )


        # --------------------------------------------------
        # Reference book
        # --------------------------------------------------

        if reference_book:

            st.subheader("Reference book")

            ref_col1, ref_col2 = st.columns(
                [1, 4]
            )

            with ref_col1:

                cover_url = reference_book.get(
                    "cover_url"
                )

                if cover_url:

                    st.image(
                        cover_url,
                        width=130
                    )

            with ref_col2:

                st.markdown(
                    f"### {reference_book.get('title', 'Unknown')}"
                )

                st.write(
                    reference_book.get(
                        "author",
                        "Unknown author"
                    )
                )

                st.caption(
                    "Used as the reference for your recommendations."
                )


        # --------------------------------------------------
        # Recommendations
        # --------------------------------------------------

        st.subheader(
            "Recommended for you"
        )

        if not recommendations:

            st.info(
                "No matching books were found. "
                "Try a broader description."
            )

        else:

            for book in recommendations:

                col1, col2 = st.columns(
                    [1, 4]
                )

                with col1:

                    cover_url = book.get(
                        "cover_url"
                    )

                    if cover_url:

                        st.image(
                            cover_url,
                            width=150
                        )

                    else:

                        st.empty()


                with col2:

                    st.markdown(
                        f"### {book.get('title', 'Unknown title')}"
                    )

                    st.markdown(
                        f"**{book.get('author', 'Unknown author')}**"
                    )

                    metadata = []

                    if book.get("year"):
                        metadata.append(
                            f"Published: {book['year']}"
                        )

                    if book.get("pages"):
                        metadata.append(
                            f"Pages: {book['pages']}"
                        )

                    if metadata:

                        st.caption(
                            " · ".join(metadata)
                        )

                    explanation = book.get(
                        "explanation",
                        ""
                    )

                    if explanation:

                        st.markdown(
                            f"**Why it matches**  \n"
                            f"{explanation}"
                        )

                    similarity = book.get(
                        "similarity"
                    )

                    if similarity is not None:

                        st.caption(
                            f"Semantic similarity: "
                            f"{similarity:.3f}"
                        )

                    book_url = book.get(
                        "book_url"
                    )

                    if book_url:

                        st.link_button(
                            "View book",
                            book_url
                        )

                st.divider()
                