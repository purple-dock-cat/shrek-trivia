import streamlit as st

st.html('''
    <div id="my-box" style="width: 200px; height: 200px; border: 1px solid black; background-color: lightblue;">
        <!-- Your box content here -->
        <script>
            // Get the box element
            var box = document.getElementById("my-box");
            
            // Add an event listener to change the background color on click
            box.addEventListener("click", function() {
                box.style.backgroundColor = "pink";
            });
        </script>
    </div>
''')