import sys
import json
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, stats, screen, sb, ship,
                         aliens, bullets):
    if event.key == pygame.K_RIGHT and not stats.level_change:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT and not stats.level_change:
        ship.moving_left = True
    elif event.key == pygame.K_UP and not stats.level_change:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN and not stats.level_change:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE and not stats.level_change:
        fire_bullets(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_RETURN and not stats.game_active:
        start_game(ai_settings, stats, screen, sb, ship, aliens, bullets)


def check_keyup_events(event, ai_settings, screen, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_play_button(ai_settings, stats, screen, sb, ship, play_button,
                      mouse_x, mouse_y, aliens, bullets):
    ''' Start a new game when player clicks Play'''
    # Collide because pygame checks for mousebuttondown anywhere on screen
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        start_game(ai_settings, stats, screen, sb, ship, aliens, bullets)


def start_game(ai_settings, stats, screen, sb, ship, aliens, bullets):
    ''' Start the game'''
    # Reset the game settings
    ai_settings.init_dynamic_settings()

    # Hide the mouse cursor
    pygame.mouse.set_visible(False)
    # Reset the game statistics
    stats.reset_stats()
    stats.game_active = True

    # Reset the scoreboard images
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()

    # Empty the list of aliens and bullets
    aliens.empty()
    bullets.empty()

    # Create a new fleet and postion the ship
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()


def check_events(ai_settings, stats, screen, sb, play_button, ship, aliens,
                 bullets):
    '''Respond to keyboard and mouse events.'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, stats, screen, sb, ship,
                                 aliens, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ai_settings, screen, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, stats, screen, sb, ship,
                              play_button, mouse_x, mouse_y, aliens, bullets)


def check_high_score(stats, sb, file):
    ''' Check to see if there is a new highscore'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
        with open(file, 'w') as f_obj:
            json.dump(stats.high_score, f_obj)


def fire_bullets(ai_settings, screen, ship, bullets):
    '''Fire a bullet within limit'''
    # Create a new bullet and add it to the bullet group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):
    ''' Determine the number of aliens that fit in a row'''
    available_space_x = ai_settings.screen_width - 2 * alien_width
    n_aliens = int(available_space_x / (2 * alien_width))
    return n_aliens


def get_number_rows(ai_settings, ship_height, alien_height):
    ''' Determine the number of rows of alien that fit the screen'''
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - (2 * ship_height))
    n_rows = int(available_space_y / (2 * alien_height))
    return n_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    '''Create an alien and place it in the row'''
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    ''' Create a full fleet of aliens'''
    alien = Alien(ai_settings, screen)
    n_aliens = get_number_aliens_x(ai_settings, alien.rect.width)
    n_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Create first row of aliens
    for row_number in range(n_rows):
        for alien_number in range(n_aliens):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    '''Drop the entire fleet and change its direction'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_screen(ai_settings, stats, screen, sb, ship, aliens, bullets,
                  play_button):
    ''' Update images on screen and flip to new screen'''
    screen.fill(ai_settings.bg_color)

    # Redraw all bullets behind ships and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Draw the scores
    sb.show_score()

    # Draw the play button if the game is inactive
    if not stats.game_active:
        play_button.draw_button()

    # Check for level change
    if ship.rect.bottom < 0:
        stats.level_change = False

    # Make the most recently drawn screen visible
    pygame.display.flip()


def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    ''' Respond to ship being hit'''
    if stats.ships_left > 0:
        # Decrement ships left
        stats.ships_left -= 1
        # Update scoreboard
        sb.prep_ships()
        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()
        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # Pause
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    ''' Check if any aliens hit the bottom'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as ship got hit
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    ''' Check if the fleet is at an edge'''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien_ship collision
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)

    # Look for aliens hitting the bottom
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)


def update_bullets(ai_settings, stats, screen, sb, ship, aliens, bullets):
    ''' Updates the position of bullets and get rid of old bullets'''
    bullets.update()

    # Delete bullets that have dissapeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collision(ai_settings, stats, screen, sb, ship, aliens,
                                 bullets)


def check_bullet_alien_collision(ai_settings, stats, screen, sb, ship, aliens,
                                 bullets):
    # Check for any bullets that have hit aliens
    # If so, get rid of bullet and alien
    # Power up bullets based on level
    if stats.level >= 4:
        ai_settings.bullet_color = (255, 0, 0)
        ai_settings.bullet_width = 10
        collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)
        scoring(ai_settings, stats, sb, collisions)
    else:
        collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
        scoring(ai_settings, stats, sb, collisions)

    # If entire fleet is destroyed start a new level
    if len(aliens) == 0:
        # Destroy existing bullets and create new fleet
        bullets.empty()
        change_level(ai_settings, stats, screen, sb, ship, aliens)
        # If ship passes top of screen means new level
        if ship.rect.bottom < 0:
            ai_settings.increase_speed()
            create_fleet(ai_settings, screen, ship, aliens)
            ship.center_ship()


def change_level(ai_settings, stats, screen, sb, ship, aliens):
    ''' Respond to changing levels'''
    stats.level += 0.5
    sb.prep_level()
    stats.level_change = True


def scoring(ai_settings, stats, sb, collisions):
    ''' To generate scores based on number of aliens hit'''
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb, stats.file_name)
