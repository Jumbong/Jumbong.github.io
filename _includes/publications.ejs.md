```{=html}
<%
const options = templateParams || {};
const selected = options.topic ? items.filter(item => item.topic === options.topic) : items;
const [feature, ...otherArticles] = selected;
const cards = options.featured ? otherArticles : selected.slice(0, options.limit || selected.length);
const heading = options.featured || options.topic ? "h3" : "h2";
const formatDate = new Intl.DateTimeFormat("fr-FR", {
  day: "numeric",
  month: "long",
  year: "numeric",
  timeZone: "UTC"
});
%>
<% if (options.featured && feature) { %>
  <article class="publication-featured">
    <a href="<%- feature.href %>">
      <div class="feature-copy">
        <p class="editorial-kicker">À la une</p>
        <p class="publication-meta">
          Towards Data Science <span aria-hidden="true">·</span>
          <time datetime="<%- feature.published %>"><%- formatDate.format(new Date(feature.published)) %></time>
        </p>
        <h2 lang="en"><%- feature.title %></h2>
        <p class="feature-description"><%- feature.summary %></p>
        <span class="feature-cta">Lire l’article <span aria-hidden="true">↗</span></span>
      </div>
      <div class="feature-image">
        <img src="<%- feature.cover %>" alt="" fetchpriority="high" referrerpolicy="no-referrer">
      </div>
    </a>
  </article>
  <div class="editorial-section-heading">
    <h2>Dernières publications</h2>
    <a class="editorial-link" href="publications.html">Toutes les publications <span aria-hidden="true">→</span></a>
  </div>
<% } %>
<div class="publication-grid">
  <% for (const item of cards) { %>
    <article class="publication-card">
      <a href="<%- item.href %>">
        <div class="publication-image">
          <img src="<%- item.cover %>" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer">
        </div>
        <div class="publication-copy">
          <p class="publication-meta">
            <span class="publication-topic"><%- item.topic %></span>
            <span aria-hidden="true">·</span>
            <time datetime="<%- item.published %>"><%- formatDate.format(new Date(item.published)) %></time>
          </p>
          <<%= heading %> lang="en"><%- item.title %></<%= heading %>>
          <p><%- item.summary %></p>
        </div>
      </a>
    </article>
  <% } %>
</div>
```
