# Node.js base image
FROM node:lts-bullseye-slim

# Working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to install dependencies
COPY package.json package-lock.json ./
RUN npm install 

# Copy the rest of the application code into the container
COPY . .

# Expose the port your app will run on
EXPOSE 3000 

# Start the app (replace 'npm start' with your start command if different)
CMD ["npm", "start"]

