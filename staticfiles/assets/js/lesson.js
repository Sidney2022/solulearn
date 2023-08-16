
    
    const Form = document.getElementById("form")
    Form.addEventListener("submit", (e) => {
        e.preventDefault()
        const formData = new FormData(form)
    
    fetch("{% url 'add-lesson' %}", {
        body: formData,
        method: "POST",
      })
        .then((res) => res.json())
        .then((data) => {
          console.log("data", data);
          console.log(data.status);
          if (data.data_error ) {
            alert("course already exists")
          }
         
        });
    })




    // Function to fetch data using AJAX
function fetchData() {
    // Make a GET request to the specified URL
    fetch("{% url 'get-lessons' course.slug %}",
    {method: "GET",}
    )
    .then(response => {
    // Check if the response was successful
    if (!response.ok) {
        throw new Error("Request failed");
    }
    // Parse the response data as JSON
    return response.json();
    })
    .then(data => {
    // Handle the response data
    //console.log(data);
    const TableBody = document.getElementById("table")
    TableBody.innerHTML = `
    <thead>
        <tr>
          <th>ID</th>
          <th>Lesson Title</th>
          <th>Lesson Conten</th>
          <th>Action</th>
         
        </tr>
      </thead>`
data.data.forEach(entry => {
    const row = TableBody.insertRow()
    const cell1 = row.insertCell(0)
    const cell2 = row.insertCell(1)
    cell1.textContent = entry['id']
    cell2.textContent = entry['title']
    cell3.textContent = entry['file']
    // Do something with the data
   // TableBody.append(lesson)
        })
    }) 
    .catch(error => {
    // Handle any errors that occurred during the request
    console.error(error);
    });
  }
  
  // Call the fetchData function initially
  fetchData();
  
  // Call the fetchData function every 5 seconds
  setInterval(fetchData, 1000);
  

