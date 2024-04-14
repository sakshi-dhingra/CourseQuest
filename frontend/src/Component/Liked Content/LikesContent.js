import React, { useState, useEffect } from 'react';

const LikesContent = () => {
  const [likedCourses, setLikedCourses] = useState([]);

  useEffect(() => {
    const fetchLikedCourses = async () => {
      try {
        const response = await fetch('http://localhost:5000/liked_courses');
        if (!response.ok) {
          throw new Error('Failed to fetch liked courses');
        }
        const data = await response.json();
        setLikedCourses(data.liked_courses);
      } catch (error) {
        console.error('Error fetching liked courses:', error);
      }
    };

    fetchLikedCourses();
  }, []);

  return (
    <div>
      <h2>Liked Courses</h2>
      <ul>
        {likedCourses.map((course, index) => (
          <li key={index}>{course}</li>
        ))}
      </ul>
    </div>
  );
};

export default LikesContent;
