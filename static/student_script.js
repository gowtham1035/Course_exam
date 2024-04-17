$(document).ready(function() {
    // Function to fetch courses data from the server
    function fetchCourses() {
        $.get('/courses', function(data) {
            // Clear existing courses
            $('#courses-list').empty();
            // Append courses to the list
            data.forEach(function(course) {
                $('#courses-list').append(`<li>${course[1]} - ${course[2]} <button class="enroll-btn" data-course="${course[1]}">Enroll</button></li>`);
            });
        });
    }

    // Fetch courses on page load
    fetchCourses();

    // Event listener for enrolling in a course
    $(document).on('click', '.enroll-btn', function() {
        var courseName = $(this).data('course');
        enrollCourse(courseName);
    });

    // Function to enroll in a course
    function enrollCourse(courseName) {
        $.post('/enroll', { course: courseName }, function(response) {
            // Refresh the courses list after enrolling
            fetchCourses();
            alert(response.message);
        });
    }
});
