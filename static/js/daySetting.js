// Function to format the date as "Month Day, Year" (e.g., "June 2, 2023")
function formatDate(date) {
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return date.toLocaleDateString('en-US', options);
}

// Function to update the label with today's date based on the provided ID
function updateTodayDateLabel(labelId) {
  const todayDateLabel = document.getElementById(labelId);
  const currentDate = new Date();
  const formattedDate = formatDate(currentDate);
  todayDateLabel.textContent = "Today's Date: " + formattedDate;
}

// Call the function to update the label with today's date
document.addEventListener("DOMContentLoaded", function() {
  updateTodayDateLabel('todayDateLabel'); // Provide the ID of the element in the respective HTML document
  updateTodayDateLabel('todayDateLabel2'); // Provide the ID of another element in a different HTML document
});
