import React, { useState, useEffect } from 'react';
import "./LikesContent.css"

const LikesContent = ({ userId }) => {
  const [likedCourses, setLikedCourses] = useState([]);

  useEffect(() => {
    const fetchLikedCourses = async () => {
      try {
        const response = await fetch(`http://localhost:5000/liked_courses/${userId}`);

        if (!response.ok) {
          throw new Error('Failed to fetch liked courses');
        }
        const data = await response.json();
        // Accumulate all liked courses
        setLikedCourses(data.liked_courses.flat()); // Use flat() to flatten the nested arrays
      } catch (error) {
        console.error('Error fetching liked courses:', error);
      }
    };
    fetchLikedCourses();
  }, [userId]); // Make sure to include userId in the dependency array to fetch data when userId changes

  return (
    <div className="liked-courses">
      <h2>Liked Courses</h2>
      <ul className="course-list">
        {likedCourses.map((course, index) => (
          <li key={index} className="course-item">
            <h3>{course['Course Name']}</h3>
            <p><strong>Difficulty Level:</strong> {course['Difficulty Level']}</p>
            <p><strong>Fees:</strong> {course['Fees']}</p>
            <p><strong>Website:</strong> {course['Website']}</p>
            <p><strong>Duration:</strong> {course['Duration']} Hours</p>
            <p><strong>Course URL:</strong> <a href={course['Course URL']} target="_blank" rel="noopener noreferrer">{course['Course URL']}</a></p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default LikesContent;
