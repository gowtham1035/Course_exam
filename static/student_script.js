$(document).ready(function() {
    // Function to fetch courses data from the server
    function fetchCourses() {
        $.get('/courses', function(data) {
            console.log(data); // Log the data received from the server
            // Clear existing courses
            $('#courses-list').empty();
            // Append courses to the list
            data.forEach(function(course) {
                // Check if course fields are defined before appending
                if (course[1] && course[2]) {
                    // Create buttons based on user role
                    let buttons = '';
                    if (course[3] === 'teacher') {
                        buttons = ''; // Teacher does not need buttons
                    } else {
                        buttons = `<button class="enroll-btn" data-id="${course[0]}">Enroll</button>
                                   <button class="drop-btn" data-id="${course[0]}">Drop</button>`;
                    }
                    $('#courses-list').append(`<li>${course[1]} - ${course[2]} ${buttons}</li>`);
                }
            });
        });
    }

    // Fetch courses on page load
    fetchCourses();

    // Event listener for creating a new course
    $('#create-course-form').submit(function(event) {
        event.preventDefault();
        var formData = $(this).serialize();
        $.post('/create_course', formData, function() {
            // Fetch courses again after creating a new course
            fetchCourses();
            $('#create-course-form').hide();
        });
    });

    // Event listener for enrolling in a course
    $(document).on('click', '.enroll-btn', function() {
        var courseId = $(this).data('id');
        $.post(`/enroll_course/${courseId}`, function() {
            // Fetch courses again after enrolling in a course
            fetchCourses();
        });
    });

    // Event listener for dropping a course
    $(document).on('click', '.drop-btn', function() {
        var courseId = $(this).data('id');
        $.post(`/drop_course/${courseId}`, function() {
            // Fetch courses again after dropping a course
            fetchCourses();
        });
    });
});
