    ---
    layout: default
    title: "Home"
    ---

    <aside class="sidebar" data-sidebar>

      <div class="sidebar-info">

        <figure class="avatar-box">
          <img src="{{ site.baseurl }}/assets/images/hedshot_1.png" alt="Tyler Kline" width="80">
        </figure>

        <div class="info-content">
          <h1 class="name" title="Tyler Kline">Tyler Kline</h1>

          <p class="title">Analytics | Product | Data Science</p>
        </div>

        <button class="info_more-btn" data-sidebar-btn>
          <span>Show Contact Info</span>

          <ion-icon name="chevron-down"></ion-icon>
        </button>

      </div>

      <div class="sidebar-info_more">

        <div class="separator"></div>

        <ul class="contacts-list">

          <li class="contact-item">

            <div class="icon-box">
              <ion-icon name="mail-outline"></ion-icon>
            </div>

            <div class="contact-info">
              <p class="contact-title">Email</p>

              <a href="mailto:tylerkline@gmail.com" class="contact-link">tylerkline@gmail.com</a>
            </div>

          </li>

          <li class="contact-item">

            <div class="icon-box">
              <ion-icon name="phone-portrait-outline"></ion-icon>
            </div>

            <div class="contact-info">
              <p class="contact-title">Phone</p>

              <a href="tel:+19525945052" class="contact-link">+1 (952) 594-5052</a>
            </div>

          </li>

          <li class="contact-item">

            <div class="icon-box">
              <ion-icon name="location-outline"></ion-icon>
            </div>

            <div class="contact-info">
              <p class="contact-title">Location</p>

              <address>New York, NY, USA</address>
            </div>

          </li>

        </ul>

        <div class="separator"></div>

        <ul class="contacts-list">

          <li class="contact-item">

            <div class="icon-box">
              <img src="{{ site.baseurl }}/assets/images/linkedin.svg" alt="LinkedIn" width="24">
            </div>

            <div class="contact-info">

              <a href="https://linkedin.com/in/tylerkline" class="contact-link">linkedin.com/in/tylerkline</a>
            </div>

          </li>

          <li class="contact-item">

            <div class="icon-box">
              <img src="{{ site.baseurl }}/assets/images/github.svg" alt="GitHub" width="24">
            </div>

            <div class="contact-info">

              <a href="https://github.com/takline" class="contact-link">github.com/takline</a>
            </div>

          </li>

        </ul>

      </div>

    </aside>

    <div class="main-content">

      <nav class="navbar">

        <ul class="navbar-list">

          <li class="navbar-item">
            <a href="{{ site.baseurl }}/about" class="navbar-link active" data-nav-link>About</a>
          </li>

          <li class="navbar-item">
            <a href="{{ site.baseurl }}/resume" class="navbar-link" data-nav-link>Resume</a>
          </li>

          <li class="navbar-item">
            <a href="{{ site.baseurl }}/projects" class="navbar-link" data-nav-link>Projects</a>
          </li>

          <li class="navbar-item">
            <a href="{{ site.baseurl }}/contact" class="navbar-link" data-nav-link>Contact</a>
          </li>

        </ul>

      </nav>
    </div>
