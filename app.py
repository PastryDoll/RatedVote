import streamlit as st
import plotly.graph_objects as go
import math

#
## Custom CSS
#

# Add new candidate button
st.markdown("""
    <style>
    .element-container:has(#button-after) + div button {
        width: 150px;
        height: 150px;
        background-color: rgba(255, 255, 255, 0);  /* Transparent background */
        border: 2px solid rgba(200, 200, 200, 0.6);  /* Light gray border */
        border-radius: 10px;
        cursor: pointer;
        display: flex;  /* Use flexbox for centering */
        justify-content: center;  /* Center horizontally */
        align-items: center;  /* Center vertically */
        position: relative;
    }
    .element-container:has(#button-after) + div button::before {
        content: "+";  /* Add the + sign */
        font-size: 80px;  /* Larger font for the + sign */
        font-weight: bold;
        color: white;  /* White color for the + sign */
        position: absolute;
    }
    .element-container:has(#button-after) + div button:hover {
        background-color: rgba(255, 255, 255, 0.1);  /* Slight gray on hover */
        border-color: rgba(255, 255, 255, 0.8);  /* Brighter border on hover */
    }
    </style>
""", unsafe_allow_html=True)

# Finish listing button
st.markdown("""
    <style>
    .element-container:has(#button-listing) + div button{
        display: block;
        width: 200px;
        height: 50px;
        margin: 0 auto; /* Center button horizontally */
        background-color: #FF4B4B; /* Red background */
        color: white;
        border: none;
        border-radius: 5px;
        font-size: 18px;
        font-weight: bold;
        cursor: pointer;
    }
    .element-container:has(#button-listing) + div button:hover {
        background-color: #FF6B6B; /* Lighten red on hover */       
    </style>
""", unsafe_allow_html=True)

# Start voting button
st.markdown("""
    <style>
    .element-container:has(#button-voting) + div button{
        display: block;
        width: 200px;
        height: 50px;
        margin: 0 auto; /* Center button horizontally */
        background-color: #FF4B4B; /* Red background */
        color: white;
        border: none;
        border-radius: 5px;
        font-size: 18px;
        font-weight: bold;
        cursor: pointer;
    }
    .element-container:has(#button-voting) + div button:hover {
        background-color: #FF6B6B; /* Lighten red on hover */
    }
    /* Style for the 'End Voting' button */
    .element-container:has(#button-end-voting) + div button {
        display: block;
        width: 200px;
        height: 50px;
        margin: 0;  /* No margin */
        background-color: #FF4B4B;
        color: white;
        border: none;
        border-radius: 5px;
        font-size: 18px;
        font-weight: bold;
        cursor: pointer;
    }
    .element-container:has(#button-end-voting) + div button:hover {
        background-color: #FF6B6B;
    }

    /* Style for the 'Next Person Voting' button */
    .element-container:has(#button-next-person) + div button {
        display: block;
        width: 200px;
        height: 50px;
        margin: 0 auto;
        background-color: #46CD11;
        color: white;
        border: none;
        border-radius: 5px;
        font-size: 18px;
        font-weight: bold;
        cursor: pointer;
    }
    .element-container:has(#button-next-person) + div button:hover {
        background-color: #4EE910;
    }

    /* Align buttons to extremes */
    .button-row {
        display: flex;
        justify-content: space-between;
    }       
    </style>
""", unsafe_allow_html=True)

# Titles 
st.markdown("""
    <style>
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #4B9CD3; /* Change title color */
        text-align: center;
        margin-bottom: 20px;
    }
    .header {
        font-size: 24px;
        font-weight: bold;
        color: #ffffff; /* Change header color */
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 
## ST state init
#
if 'candidates' not in st.session_state:
    st.session_state['candidates'] = []
    
if 'votes' not in st.session_state:
    st.session_state['votes'] = {}

if 'show_form' not in st.session_state:
    st.session_state['show_form'] = False  

if 'listing' not in st.session_state:
    st.session_state['listing'] = True

if 'voting' not in st.session_state:
    st.session_state['voting'] = False

if 'new_voter' not in st.session_state:
    st.session_state["new_voter"] = False

if 'total_voters' not in st.session_state:
    st.session_state['total_voters'] = 0

if 'statistics' not in st.session_state:
    st.session_state['statistics'] = False
#
## Register Buttons Callbacks
#
def add_candidate(name, picture, description):
    if name not in [candidate['name'] for candidate in st.session_state['candidates']]:
        st.session_state['candidates'].append({
            'name': name,
            'picture': picture,
            'description': description
        })
        st.session_state['show_form'] = False
        return True
    else:
        st.warning(f"Candidate '{name}' already exists. Please choose a different name.")
        return False

def delete_candidate(index):
    del st.session_state['candidates'][index]

def show_add_form():
    st.session_state['show_form'] = True

def hide_add_form():
    st.session_state['show_form'] = False

def finish_listing():
    st.session_state["listing"] = False
    for cadidates in st.session_state["candidates"]:
        print(cadidates)
        st.session_state['votes'][cadidates["name"]] = {"approvals": 0, "disaprovals":0, "rating":0}

def start_voting():
    st.session_state["voting"] = True

def next_voter():
    st.session_state["new_voter"] = True

def end_vote():
    st.session_state["new_voter"] = True
    st.session_state['voting'] = False
    st.session_state["statistics"] = True

if st.session_state["listing"] and not st.session_state["voting"]:
    #
    ## UI Header
    #

    st.markdown('<div class="title">Candidate Rating Vote App</div>', unsafe_allow_html=True)
    if len(st.session_state['candidates']) > 0:
        st.markdown('<span id="button-listing"></span>', unsafe_allow_html=True)
        st.button("Finish Listing", on_click=finish_listing)
    st.markdown('<div class="header">Candidates List:</div>', unsafe_allow_html=True)

    # 
    ## UI List of candidates
    #

    num_cols = 3
    cols = st.columns(num_cols)
    num_candidates = len(st.session_state['candidates'])

    with cols[0]:
        st.markdown('<span id="button-after"></span>', unsafe_allow_html=True)
        st.button(" ", key="add_button", help="Click to add a new candidate", on_click=show_add_form)

    for idx, candidate in enumerate(st.session_state['candidates']):
        col_idx = (idx + 1) % num_cols  
        if col_idx == 0:
            cols = st.columns(num_cols)  
        with cols[col_idx]:
            st.subheader(f"{candidate['name']}")
            if candidate['picture'] is not None:
                st.image(candidate['picture'], width=150)
            if candidate['description']:
                formatted_description = candidate['description'].replace('\n', '<br>') 
                st.markdown(
                    f"""
                    <div style='font-size:14px; color:#E3E2E2;'>
                    <strong>Description:</strong><br> {formatted_description}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            st.button(f"Delete {candidate['name']}", key=f"delete_{idx}", on_click=delete_candidate, args=(idx,))

    #
    ## SideBar form for adding candidate
    #
    if st.session_state['show_form']:
        with st.sidebar.form(key='candidate_form'):
            st.header("Add a New Candidate")
            new_candidate_name = st.text_input("Candidate Name")
            new_candidate_description = st.text_area("Candidate Description (optional)", help="A brief description of the candidate")
            new_candidate_picture = st.file_uploader("Upload Candidate Picture (optional)", type=["jpg", "jpeg", "png"])

            if st.form_submit_button("Add Candidate"):
                if new_candidate_name:
                    if add_candidate(new_candidate_name, new_candidate_picture, new_candidate_description):
                        hide_add_form()
                        st.rerun()
                else:
                    st.sidebar.warning("Please enter a candidate name")
            if st.sidebar.button("Cancel"):
                hide_add_form()

elif not st.session_state["listing"] and not st.session_state["voting"] and not st.session_state["statistics"]:
    st.markdown('<span id="button-voting"></span>', unsafe_allow_html=True)
    st.button("Start Voting", on_click=start_voting)

elif st.session_state["voting"]:
    st.markdown('<div class="button-row"></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.markdown('<span id="button-end-voting"></span>', unsafe_allow_html=True)
        st.button("End Voting", on_click=end_vote)

    with col2:
        pass

    with col3:
        st.markdown('<span id="button-next-person"></span>', unsafe_allow_html=True)
        if st.button("Next Person Voting", on_click=next_voter):
            st.success("Votes reset for the next person!")

    st.markdown("""
        <div style="font-size:16px; color:#dddddd;">
        Please rate each candidate on a scale from -10 to +10. Move the slider to assign a score to each candidate.
        </div>
        """, unsafe_allow_html=True)

    for i, candidate in enumerate(st.session_state['candidates']):
        st.markdown("<hr>", unsafe_allow_html=True) 
        st.subheader(candidate['name'])
        col1, col2 = st.columns([2, 1])  
        
        with col1:
            if candidate['picture'] is not None:
                st.image(candidate['picture'], width=150)
            if candidate['description']:
                formatted_description = candidate['description'].replace('\n', '<br>') 
                st.markdown(
                    f"""
                    <div style='font-size:14px; color:#E3E2E2;'>
                    <strong>Description:</strong><br> {formatted_description}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with col2:
            rating = st.slider(
                f"Rate {candidate['name']} (-10 to +10):",
                min_value=-10,
                max_value=10,
                key=f"rating_{candidate['name']}_{i}_{st.session_state['total_voters']}",
                value = 0
            )
            print(rating)
        if st.session_state["new_voter"]:
            if rating >= 0:
                st.session_state['votes'][candidate['name']]["approvals"] += rating
            else:
                st.session_state['votes'][candidate['name']]["disaprovals"] -= rating
            st.session_state['votes'][candidate['name']]["rating"] = st.session_state['votes'][candidate['name']]["approvals"] - st.session_state['votes'][candidate['name']]["disaprovals"]
            print(st.session_state['votes'][candidate['name']])
            if i == len(st.session_state['candidates']) - 1:
                st.session_state["new_voter"] = False
                st.session_state["total_voters"] += 1
                st.rerun()
    
elif st.session_state.get("statistics", False):
    st.markdown("<div style='color:green; font-size:18px;'>Voting has ended. Thank you for participating!</div>", unsafe_allow_html=True)
    
    winner_rating = -11
    winner = {}
    
    for candidate in st.session_state['candidates']:
        vote = st.session_state['votes'][candidate["name"]]
        if vote["rating"] > winner_rating:
            winner_rating = vote["rating"]
            winner = candidate

    if winner:
        st.markdown(f"""
            <h3>The winner is <strong style='color:gold;'>{winner['name']}</strong> with a rating of {winner_rating}!</h3>
            """, unsafe_allow_html=True)
        if winner['picture'] is not None:
            st.image(winner['picture'], width=640)
    
    st.markdown(f"<h4>Total number of voters: {st.session_state['total_voters']}</h4>", unsafe_allow_html=True)

    candidates = [candidate['name'] for candidate in st.session_state['candidates']]
    approvals = [st.session_state['votes'][candidate]['approvals'] for candidate in candidates]
    disapprovals = [st.session_state['votes'][candidate]['disaprovals'] for candidate in candidates]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=candidates, 
        y=approvals, 
        name='Approvals',
        marker_color='green'
    ))

    fig.add_trace(go.Bar(
        x=candidates, 
        y=disapprovals, 
        name='Disapprovals',
        marker_color='red'
    ))

    fig.update_layout(
        title={
            'text': 'Approval vs Disapproval by Candidate',
            'x': 0.5,  
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_tickangle=-45,
        barmode='group',
        yaxis_title='Votes',
        xaxis_title='Candidates',
        template='plotly_dark',  
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        legend=dict(
            x=0.85, y=1.15,
            bgcolor='rgba(255,255,255,0.1)',
            bordercolor='rgba(255,255,255,0.1)'
        ),
        xaxis=dict(
            showgrid=True,  
            gridcolor='rgba(255,255,255,0.2)'  
        )
    )

    st.plotly_chart(fig)




