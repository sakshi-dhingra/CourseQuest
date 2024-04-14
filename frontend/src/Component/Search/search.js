import React, { useState,useEffect } from 'react';
import './search.css'; 
import Select from 'react-select';

const Search = ({ onSearch }) => {
  const [selectedAttributes, setSelectedAttributes] = useState([]);
  const [selectedDifficulty, setSelectedDifficulty] = useState('');
  const [selectedWebsite, setSelectedWebsite] = useState('');
  const [selectedPaid, setSelectedPaid] = useState('');
  const [keywords, setKeywords] = useState([]);
  const [recommendedCourses, setRecommendedCourses] = useState(null);


  useEffect(() => {
    const fetchKeywords = async () => {
      try {
        const response = await fetch('http://localhost:5000/keywords');
        if (!response.ok) {
          throw new Error('Failed to fetch keywords');
        }
        const data = await response.json();
        const options = data.keywords.map(keyword => ({ value: keyword, label: keyword }));
        setKeywords(options);
      } catch (error) {
        console.error('Error fetching keywords:', error);
      }
    };

    fetchKeywords();
  }, []); 


  // Options for dropdown questions
  const difficultyOptions = ['Beginner', 'Intermediate', 'Advanced'];
  const websiteOptions = ['Coursera','EdX','Both'];
  const paidOptions = ['Paid', 'Unpaid','Both'];

  // Event handlers for dropdown selections
  const handleAttributeChange = (selectedOptions) => {
    setSelectedAttributes(selectedOptions);
  };
  const handleDifficultyChange = (event) => {
    setSelectedDifficulty(event.target.value);
  };

  const handleWebsiteChange = (event) => {
    setSelectedWebsite(event.target.value);
  };

  const handlePaidChange = (event) => {
    setSelectedPaid(event.target.value);
  };

  // Function to handle search submission
  const handleSearchSubmit = async (event) => {
    event.preventDefault();
    const searchParams = {
      attributes: selectedAttributes.map(option => option.value),
      difficulty: selectedDifficulty,
      website: selectedWebsite,
      paid: selectedPaid,
    };
  
    try {
      const response = await fetch('http://localhost:5000/generate_recommendations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(searchParams)
      });
  
      if (!response.ok) {
        throw new Error('Failed to fetch recommendations');
      }
  
      const data = await response.json();
      console.log('Recommended courses:', data.recommended_courses);
      setRecommendedCourses(data.recommended_courses);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    }

  };


  const handleLikeCourse = async courseName => {
    try {
      const response = await fetch('http://localhost:5000/like_course', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ course_name: courseName })
      });

      if (!response.ok) {
        throw new Error('Failed to like course');
      }

      // Handle success
    } catch (error) {
      console.error('Error liking course:', error);
    }
  };

  return (
    <div className="search-container">
      <h2>Search Courses</h2>
      <form onSubmit={handleSearchSubmit} className="search-form">
      <div className="form-group">
          <label>Attributes:</label>
          <Select
            isMulti
            value={selectedAttributes}
            onChange={handleAttributeChange}
            options={keywords}
          />
      </div>  
        {/* Dropdown for Difficulty level */}
        <div className="form-group">
          <label>Difficulty Level:</label>
          <select value={selectedDifficulty} onChange={handleDifficultyChange}>
            <option value="">Select Difficulty</option>
            {difficultyOptions.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </div>
        {/* Dropdown for Website */}
        <div className="form-group">
          <label>Website:</label>
          <select value={selectedWebsite} onChange={handleWebsiteChange}>
            <option value="">Select Website</option>
            {websiteOptions.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </div>
        {/* Dropdown for Paid/Unpaid */}
        <div className="form-group">
          <label>Cost:</label>
          <select value={selectedPaid} onChange={handlePaidChange}>
            <option value="">Select Cost</option>
            {paidOptions.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </div>
        <button type="submit" className="search-button">Search</button>
      </form>
  {recommendedCourses && recommendedCourses.length > 0 && (
  <div className="recommended-courses">
    <h3>Recommended Courses</h3>
    <hr></hr>
    <div className="courses-list">
      {recommendedCourses.map((course, index) => (
        <div key={index} className="course">
          <h4>{course['Course Name']}</h4>
          <p><strong>Difficulty Level:</strong> {course['Difficulty Level']}</p>
          <p><strong>Fees:</strong> {course['Fees']}</p>
          <p><strong>Website:</strong> {course['Website']}</p>
          <p><strong>Course URL:</strong> <a href={course['Course URL']} target="_blank" rel="noopener noreferrer">{course['Course URL']}</a></p>
          <button onClick={() => handleLikeCourse(course['Course Name'])}>
                  Like
          </button>
          {index !== recommendedCourses.length - 1 && <hr />} 
        </div>
      ))}
    </div>
  </div>
)}
    </div>
  );
};

export default Search;
 