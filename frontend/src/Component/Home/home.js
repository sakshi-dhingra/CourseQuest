import React, { useState } from 'react';
import './home.css';
import Search from '../Search/search.js'; 
import userProfileIcon from './static/user_icon.png';
import { useLocation } from 'react-router-dom';
import LikesContent from '../Liked Content/LikesContent.js'; 
import Similar from '../SimilarCourses/Similar.js'



const Home = ({ userId }) => {
  const [selectedTab, setSelectedTab] = useState('search');
  const location = useLocation();
  const username = location.state && location.state.username ? location.state.username : '';

  console.log("Location state:", location.state);
  console.log("User ID:", userId); 
  const handleTabClick = (tab) => {
    setSelectedTab(tab);
  };

  const renderTabContent = () => {
    switch (selectedTab) {
      case 'search':
        return <Search userId={userId}/>; 
      case 'likes':
        return <LikesContent userId={userId} />;
      case 'similar':
        return <Similar userId={userId} /> 
      default:
        return null;
    }
  };

  return (
    <div className="home-container">
      <div className="user-profile">
        {/* User profile icon */}
        <img src={userProfileIcon} alt="User Profile" className="user-profile-icon" />        {/* User name */}
        <span className="user-name">{username}</span>
      </div>
      <h1>Welcome to CourseQuest</h1>
      <h3>Redefining Courses searching for you...</h3>
      <h3>Created by Adaptive System Students (Group Athena)</h3>

      {/* Render tabs */}
      <div className="tabs">
        <div className={`tab ${selectedTab === 'search' ? 'active' : ''}`} onClick={() => handleTabClick('search')}>Search</div>
        <div className={`tab ${selectedTab === 'likes' ? 'active' : ''}`} onClick={() => handleTabClick('likes')}>Likes</div>
        <div className={`tab ${selectedTab === 'similar' ? 'active' : ''}`} onClick={() => handleTabClick('similar')}>Similar</div>
      </div>

      {/* Render content based on selected tab */}
      <div className="tab-content">
        {renderTabContent()}
      </div>
    </div>
  );
};


export default Home;
