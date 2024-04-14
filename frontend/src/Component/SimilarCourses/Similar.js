import React, { useState, useEffect } from 'react';
import './Similar.css';

const Similar = ({ userId }) => {
  const [similarCourses, setSimilarCourses] = useState([]);

  useEffect(() => {
    const fetchSimilarCourses = async () => {
      try {
        const response = await fetch(`http://localhost:5000/similar_courses/${userId}`);
        if (!response.ok) {
          throw new Error('Failed to fetch similar courses');
        }
        const data = await response.json();
        setSimilarCourses(data.similar_courses);
      } catch (error) {
        console.error('Error fetching similar courses:', error);
      }
    };

    if (userId) {
      fetchSimilarCourses();
    }
  }, [userId]);

  return (
    <div className="similar-container">
      <h2>Similar Courses</h2>
      <ul>
        {similarCourses.map((course, index) => (
          <li key={index}>
            <div className="course">
              <h4>{course['Course Name']}</h4>
              <p><strong>Difficulty Level:</strong> {course['Difficulty Level']}</p>
              <p><strong>Fees:</strong> {course['Fees']}</p>
              <p><strong>Website:</strong> {course['Website']}</p>
              <p><strong>Course URL:</strong> <a href={course['Course URL']} target="_blank" rel="noopener noreferrer">{course['Course URL']}</a></p> 
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Similar;
