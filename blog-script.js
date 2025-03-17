// Blog System JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Only run this code if the blog container exists
    const blogContainer = document.getElementById('blogPostsContainer');
    if (!blogContainer) return;

    // Function to generate a random rotation between -2 and 2 degrees
    function getRandomRotation() {
        return (Math.random() * 4 - 2).toFixed(2) + 'deg';
    }

    // Function to fetch blog posts
    async function fetchBlogPosts() {
        try {
            const response = await fetch('/blog/blog-data.json');
            if (!response.ok) {
                throw new Error('Failed to fetch blog posts');
            }
            
            const data = await response.json();
            return data.posts;
        } catch (error) {
            console.error('Error fetching blog posts:', error);
            return [];
        }
    }

    // Function to create blog post card
    function createBlogPostCard(post) {
        const rotation = getRandomRotation();
        
        const card = document.createElement('div');
        card.className = 'blog-card';
        card.style.setProperty('--random-rotation', rotation);
        
        const content = `
            <div class="blog-image-container">
                <img src="${post.thumbnail}" alt="${post.title}" class="blog-image">
            </div>
            <div class="blog-content">
                <h3 class="blog-title">${post.title}</h3>
                <div class="blog-date">${post.date}</div>
                <p class="blog-excerpt">${post.excerpt}</p>
                <a href="/blog/posts/${post.slug}.html" class="blog-link">read more</a>
            </div>
        `;
        
        card.innerHTML = content;
        return card;
    }

    // Load blog posts
    async function loadBlogPosts() {
        const posts = await fetchBlogPosts();
        
        if (posts.length === 0) {
            blogContainer.innerHTML = '<p class="loading-posts">No posts found</p>';
            return;
        }
        
        // Clear loading message
        blogContainer.innerHTML = '';
        
        // Sort posts by date (newest first)
        posts.sort((a, b) => new Date(b.date) - new Date(a.date));
        
        // Add the latest 5 posts to the container
        const latestPosts = posts.slice(0, 5);
        latestPosts.forEach(post => {
            const card = createBlogPostCard(post);
            blogContainer.appendChild(card);
        });
        
        // Initialize horizontal scrolling
        initHorizontalScroll();
    }

    // Initialize horizontal scrolling with arrow buttons
    function initHorizontalScroll() {
        const scrollContainer = document.querySelector('.blog-posts-wrapper');
        const leftArrow = document.querySelector('.scroll-left');
        const rightArrow = document.querySelector('.scroll-right');
        
        if (!scrollContainer || !leftArrow || !rightArrow) return;
        
        leftArrow.addEventListener('click', () => {
            scrollContainer.scrollBy({ left: -320, behavior: 'smooth' });
        });
        
        rightArrow.addEventListener('click', () => {
            scrollContainer.scrollBy({ left: 320, behavior: 'smooth' });
        });
    }

    // Load the posts
    loadBlogPosts();
});
