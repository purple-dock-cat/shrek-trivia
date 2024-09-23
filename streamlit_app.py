import streamlit as st

# Create a canvas component
canvas = st.canvas(key="rectangle_canvas")

# Draw a rectangle on the canvas
canvas.rect(100, 100, 200, 200, fill_color="blue")

# Add JavaScript code to handle swipe events
script = """
<script>
  // Get the canvas element
  var canvas = document.getElementById("rectangle_canvas");

  // Add event listeners for swipe gestures
  canvas.addEventListener("touchstart", handleTouchStart, false);
  canvas.addEventListener("touchmove", handleTouchMove, false);

  // Variables to track swipe direction
  var swipeDirection = null;
  var swipeStartX = null;

  // Handle touch start event
  function handleTouchStart(event) {
    swipeStartX = event.touches[0].clientX;
  }

  // Handle touch move event
  function handleTouchMove(event) {
    var swipeEndX = event.touches[0].clientX;
    var swipeDistance = swipeEndX - swipeStartX;

    // Determine swipe direction
    if (swipeDistance > 50) {
      swipeDirection = "right";
    } else if (swipeDistance < -50) {
      swipeDirection = "left";
    }

    // Update the rectangle's position based on swipe direction
    if (swipeDirection === "right") {
      canvas.style.left = (parseInt(canvas.style.left) + 10) + "px";
    } else if (swipeDirection === "left") {
      canvas.style.left = (parseInt(canvas.style.left) - 10) + "px";
    }
  }
</script>
"""

# Add the script to the app
st.markdown(script, unsafe_allow_html=True)