// Function to delete a job with a specified 'id'
// it will take the job id ('id') as an argument
function deleteJob(jobID) {
  // and will send a 'post' request to the '/delete-job' endpoint using the Fetch API
  fetch(
    "/delete-job", // The URL to send the request to
    {
      method: "POST", // The HTTP method for the request
      body: JSON.stringify({ jobID: jobID }) // where the request body containing the 'id' a JS object ({ id: '123' }) converted into JSON string format ({"id":"123"})
    }
    // after the request is complete (regardless of the response), it will reload/refresh or redirect the window
  ).then((_res) => {
    window.location.href = "/";
  });
}

// this is all we need to delete the job posting. And this is just how you send a really basic, request to the backend from JavaScript
