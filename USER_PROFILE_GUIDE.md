# 👤 User Profile & Time Tracking - Feature Guide

## 🎯 **Feature Overview**
The User Profile feature tracks how much time users spend on the AI Crop Diseases Solution website, providing detailed analytics about user engagement and activity patterns.

---

## 🌟 **Key Features**

### **📊 Visit Statistics:**
- **Total Visits** - Number of times user has logged in
- **Total Sessions** - Number of browsing sessions
- **Total Time Spent** - Cumulative time across all sessions
- **Average Session Duration** - Average time per session

### **📈 Recent Activity:**
- **Last 7 Days** - Recent sessions and time spent
- **Session History** - Last 10 sessions with details
- **Page Views** - Number of pages visited per session
- **Real-time Tracking** - Live session duration updates

---

## 🔧 **Technical Implementation**

### **Database Models:**

#### **UserProfile Model:**
```python
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_visits = models.IntegerField(default=0)
    total_time_spent = models.IntegerField(default=0)  # in seconds
    last_visit = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

#### **UserSession Model:**
```python
class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_start = models.DateTimeField(auto_now_add=True)
    session_end = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(default=0)  # in seconds
    pages_visited = models.IntegerField(default=0)
```

### **Middleware Tracking:**
- **UserTrackingMiddleware** - Automatically tracks user activity
- **Session Management** - Handles session start/end times
- **Page Counting** - Tracks pages visited per session
- **Time Calculation** - Real-time duration updates

---

## 🌐 **User Interface**

### **Profile Page URL:**
```
http://127.0.0.1:8000/profile/
```

### **Navigation Access:**
- **Main Page** - Profile button in header navigation
- **Database Page** - Profile link in navigation menu
- **Direct URL** - `/profile/` endpoint

### **Profile Page Sections:**

#### **1. User Information Card:**
- **Profile Avatar** - User icon with initials
- **Full Name** - First and last name
- **Username** - @username display
- **Member Since** - Account creation date

#### **2. Statistics Grid:**
- **Total Visits** - Lifetime visit count
- **Sessions** - Total session count
- **Total Time** - Formatted time display (hours, minutes, seconds)
- **Average Session** - Average duration per session

#### **3. Recent Activity:**
- **7-Day Summary** - Recent sessions and time
- **Session History** - Last 10 sessions with:
  - Date and time
  - Session duration
  - Pages visited

---

## 📱 **User Experience Features**

### **Professional Design:**
- **Agricultural Theme** - Consistent with app design
- **Responsive Layout** - Works on all devices
- **Real-time Updates** - Auto-refresh every 30 seconds
- **Clean Typography** - Easy to read statistics

### **Time Formatting:**
- **Smart Display** - Shows hours, minutes, seconds as appropriate
- **Human Readable** - "2h 15m 30s" format
- **Zero Handling** - Graceful display of no activity

### **Activity Indicators:**
- **Active Sessions** - Shows "Active" for current session
- **Color Coding** - Green badges for time spent
- **Icons** - Font Awesome icons for visual appeal

---

## 🔍 **How It Works**

### **Session Tracking Process:**

#### **1. User Login:**
- Middleware detects authenticated user
- Creates or updates UserProfile
- Increments total visit count
- Starts new UserSession record

#### **2. Page Navigation:**
- Each page request tracked
- Session duration updated in real-time
- Page visit count incremented
- Last activity timestamp updated

#### **3. Time Calculation:**
- Start time recorded on session creation
- Duration calculated on each request
- Total time accumulated in UserProfile
- Average calculated from all sessions

#### **4. Session End:**
- Automatic timeout after inactivity
- Final duration saved to database
- Session marked as completed

---

## 📊 **Analytics & Insights**

### **User Engagement Metrics:**
- **Visit Frequency** - How often users return
- **Session Length** - How long users stay
- **Page Engagement** - Pages viewed per session
- **Activity Patterns** - Recent vs historical usage

### **Time Tracking Accuracy:**
- **Real-time Updates** - Live session tracking
- **Reasonable Limits** - Prevents unrealistic time counts
- **Session Validation** - Handles browser refresh/navigation
- **Data Integrity** - Consistent time calculations

---

## 🎯 **Business Value**

### **User Insights:**
- **Engagement Levels** - Understand user behavior
- **Feature Usage** - Track popular sections
- **Return Patterns** - Identify loyal users
- **Time Investment** - Measure user commitment

### **Agricultural Impact:**
- **Learning Time** - How long users spend learning
- **Research Patterns** - Disease lookup frequency
- **Knowledge Building** - Progressive engagement
- **Platform Stickiness** - User retention metrics

---

## 🔧 **Technical Features**

### **Performance Optimized:**
- **Efficient Queries** - Minimal database impact
- **Session Caching** - Fast middleware processing
- **Batch Updates** - Optimized time tracking
- **Error Handling** - Graceful failure management

### **Security & Privacy:**
- **User-Specific Data** - Only own profile visible
- **Login Required** - Protected endpoints
- **Session Security** - Secure session management
- **Data Protection** - No sensitive information exposed

---

## 🚀 **Future Enhancements**

### **Potential Features:**
- **Weekly/Monthly Reports** - Extended analytics
- **Activity Heatmaps** - Visual usage patterns
- **Goal Setting** - Learning time targets
- **Achievements** - Engagement milestones
- **Export Data** - Download activity reports

### **Advanced Analytics:**
- **Page-Level Tracking** - Time per page
- **Feature Usage** - Search vs browse patterns
- **Mobile vs Desktop** - Device usage analytics
- **Peak Hours** - Usage time analysis

---

## 📋 **Usage Instructions**

### **For Users:**
1. **Login** to your account
2. **Click Profile** in the navigation menu
3. **View Statistics** - See your activity summary
4. **Check Recent Activity** - Review last 10 sessions
5. **Monitor Progress** - Track learning time

### **For Administrators:**
1. **Access Django Admin** - View all user profiles
2. **Monitor Engagement** - Check user activity levels
3. **Analyze Patterns** - Understand usage trends
4. **Optimize Features** - Based on usage data

---

## 🎉 **Benefits Summary**

### **For Users:**
- **Track Learning Progress** - See time invested in agricultural knowledge
- **Monitor Engagement** - Understand your usage patterns
- **Professional Profile** - Clean, informative interface
- **Motivation** - Visual progress tracking

### **For Platform:**
- **User Analytics** - Understand engagement levels
- **Feature Optimization** - Data-driven improvements
- **User Retention** - Identify engagement patterns
- **Agricultural Impact** - Measure learning outcomes

**Your AI Crop Diseases Solution now includes comprehensive user profile and time tracking features!** 🌾📊✨
