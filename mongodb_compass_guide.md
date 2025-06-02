# 🧭 MongoDB Compass - Manual Disease Addition Guide

## 📊 **Using MongoDB Compass to Add Diseases**

### **1. 🔗 Connect to MongoDB**
1. **Download & Install:** https://www.mongodb.com/products/compass
2. **Launch** MongoDB Compass
3. **Connection String:** `mongodb://localhost:27017`
4. **Click Connect**

### **2. 📁 Navigate to Database**
1. **Select Database:** `plant_diseases`
2. **Select Collection:** `diseases`
3. **Click** "Insert Document" button

### **3. 📝 Add Disease Document**

**Sample Disease Document Structure:**
```json
{
  "name": "your_disease_name",
  "description": "Disease description here",
  "solutions": [
    {
      "type": "organic",
      "solution": "Treatment description",
      "effectiveness": "High",
      "application": "How to apply"
    },
    {
      "type": "inorganic", 
      "solution": "Chemical treatment",
      "effectiveness": "Very High",
      "application": "Application method"
    }
  ],
  "added_date": "2025-06-01T14:00:00.000Z",
  "added_manually": true
}
```

### **4. 📋 Example Diseases to Add**

**Tomato Blight:**
```json
{
  "name": "tomato blight",
  "description": "A devastating disease affecting tomato plants, causing dark spots on leaves and fruit rot",
  "solutions": [
    {
      "type": "organic",
      "solution": "Copper sulfate spray with baking soda",
      "effectiveness": "High", 
      "application": "Spray every 7 days in early morning"
    },
    {
      "type": "inorganic",
      "solution": "Chlorothalonil fungicide",
      "effectiveness": "Very High",
      "application": "Apply every 10-14 days during growing season"
    }
  ],
  "added_date": "2025-06-01T14:00:00.000Z",
  "added_manually": true
}
```

**Cucumber Mosaic Virus:**
```json
{
  "name": "cucumber mosaic virus",
  "description": "Viral disease causing mottled yellow and green patterns on leaves",
  "solutions": [
    {
      "type": "organic",
      "solution": "Remove infected plants and control aphid vectors",
      "effectiveness": "Medium",
      "application": "Immediate removal and disposal of infected plants"
    },
    {
      "type": "inorganic",
      "solution": "Systemic insecticide for aphid control",
      "effectiveness": "High", 
      "application": "Apply to prevent aphid transmission"
    }
  ],
  "added_date": "2025-06-01T14:00:00.000Z",
  "added_manually": true
}
```

### **5. ✅ Validation Rules**

**Required Fields:**
- `name` (string, lowercase)
- `description` (string)
- `solutions` (array with at least 1 solution)

**Solution Fields:**
- `type` ("organic" or "inorganic")
- `solution` (string, treatment description)
- `effectiveness` ("Low", "Medium", "High", "Very High")
- `application` (string, how to apply)

### **6. 🔍 Query Examples**

**Find all organic solutions:**
```json
{ "solutions.type": "organic" }
```

**Find diseases by name:**
```json
{ "name": { "$regex": "mildew", "$options": "i" } }
```

**Find manually added diseases:**
```json
{ "added_manually": true }
```
