import React, { useState } from 'react';
import './search.css'; 

const Search = ({ onSearch }) => {
  const [userInputAttributes, setUserInputAttributes] = useState('');
  const [selectedDifficulty, setSelectedDifficulty] = useState('');
  const [selectedWebsite, setSelectedWebsite] = useState('');
  const [selectedPaid, setSelectedPaid] = useState('');

  // Options for dropdown questions
  const difficultyOptions = ['Begginer', 'Intermediate', 'Advanced'];
  const websiteOptions = ['Coursera','Edx'];
  const paidOptions = ['Paid', 'Unpaid'];

  // Event handlers for dropdown selections
  const handleAttributeChange = (event) => {
    setUserInputAttributes(event.target.value);
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
  const handleSearchSubmit = (event) => {
    event.preventDefault();
    const searchParams = {
      attributes: userInputAttributes,
      difficulty: selectedDifficulty,
      website: selectedWebsite,
      paid: selectedPaid,
    };
    // Call the onSearch function passed from the parent component with search parameters
    onSearch(searchParams);
  };

  return (
    <div className="search-container">
      <h2>Search Courses</h2>
      <form onSubmit={handleSearchSubmit} className="search-form">
        {/* Dropdown for Attributes */}
        <div className="form-group">
          <label>Attributes:</label>
          <input type="text" value={userInputAttributes} onChange={handleAttributeChange} placeholder="Enter attributes" />
        </div>
        {/* Dropdown for Difficulty level */}
        <div className="form-group">
          <label>Difficulty level:</label>
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
          <label>Paid/Unpaid:</label>
          <select value={selectedPaid} onChange={handlePaidChange}>
            <option value="">Select Paid/Unpaid</option>
            {paidOptions.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </div>
        <button type="submit" className="search-button">Search</button>
      </form>
    </div>
  );
};

export default Search;
 