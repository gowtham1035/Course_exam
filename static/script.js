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
                    $('#courses-list').append(`<li>${course[1]} - ${course[2]} <button class="drop-btn" data-id="${course[0]}">Drop</button></li>`);
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

    // Event listener for dropping a course
    $(document).on('click', '.drop-btn', function() {
        var courseId = $(this).data('id');
        $.post(`/drop_course/${courseId}`, function() {
            // Fetch courses again after dropping a course
            fetchCourses();
        });
    });

    // Event listener for add course button
    $('#add-course-btn').click(function() {
        $('#create-course-form').show();
    });

    // Event listener for delete course button
    $('#delete-course-btn').click(function() {
        $('.drop-btn').toggle();
    });
});
