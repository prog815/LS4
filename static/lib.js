function get_link() {
    return "с сервера" ;
}

function search(page_number,func) {
    
    // Define the URL of the REST API endpoint
    const url = 'http://localhost/search';
  
    // Define the request options, including the query parameter in the URL
    const options = {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    };
  
    // Send the request using the fetch() function
    fetch(url + '?page_number=' + page_number, options)
      .then(response => response.json())
      .then(data => {
        console.log(data)
      })
      .catch(error => {
        // Handle any errors that occur during the request
        console.error(error);
      });
  }
  