import streamlit as st
import requests


def search_topmate(searchterm: str):
    if not searchterm:
        return []

    response = requests.get(
        "https://fuzzy-coder.gravitron.run/semantic-search/",
        params={
            "query": searchterm,
        },
        timeout=30,
    ).json()

    print(response)
    return response


EXPERT_HTML_TEMPLATE = """
<div class="card text-white bg-dark mb-3" style="width: 36rem;">
  <img src="{}" class="card-img-top" alt=""/>
  <div class="card-body">
    <h5 class="card-title">{}</h5>
	<a href="{}" target="_blank" class="card-link">{}</a>
  </div>
</div>
"""


def main():
    st.title("Topmate Search")
    st.markdown(
        '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">',
        unsafe_allow_html=True,
    )
    with st.form(key="searchform"):
        nav1, nav2 = st.columns([2, 1])

        with nav1:
            search_term = st.text_input("Eg: experts working at google")

        with nav2:
            submit_search = st.form_submit_button(label="Search")

    (col1,) = st.columns([1])

    with col1:
        if not submit_search:
            return
        
        data = search_topmate(search_term)
        if data and 'detail' in data:
            st.subheader("Unable to find any relevant experts associated to your query")
            return

        st.subheader("Showing {} experts".format(len(data)))
        for user in data:
            st.markdown(
				EXPERT_HTML_TEMPLATE.format(
					user.get("profile_pic"),
					user.get("display_name"),
					f'https://topmate.io/{user.get("username")}',
					user.get("username"),

				),
				unsafe_allow_html=True,
			)


if __name__ == "__main__":
    main()
