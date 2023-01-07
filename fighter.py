import pygame

class Fighter():
  def __init__(self, x, y, flip, data, sprite_sheet, animation_steps):
    self.size = data[0] # it will start from the 0th position of the sprite sheet
    self.image_scale = data[1] #Used for scaling the images. At first the images will appear as small. After using it we will get a scaled up version of the images.
    self.offset = data[2] # This one is used because at first without these the image of the objects will be at different coordinates than we want. to move these guys back into the main position, we want the offset. The main position co-ordinate is defined in the WARRIER_OFFSET variable in main.py file.
    self.animation_list = self.load_images(sprite_sheet, animation_steps) # Here in the begining itself we are using the 'load_images' method so that from the spritesheet we can get a list in the begning itself
    self.flip = flip  #In the fighter class we need to know the players are facing each other. If self.flip = False -> only the warrior will be facing properly but the wizard will not face properly. so we use self.flip = flip.
    self.rect = pygame.Rect((x, y, 80, 180)) # pygame will create a rectangular object at 'x' and 'y' co-ordinate. Its height will be 80 pixels and width will ne 100 pixels.
    self.vel_y = 0 #for jumping
    self.action = 0  # what the character is actually doing:- 0:idle #1:run #2:jump #3:attack1 #4: attack2 #5:hit #6:death
    self.frame_index = 0
    self.image = self.animation_list[self.action][self.frame_index]
    # self.image_scale = data[1]
    self.jump = False  # If we don't use this , then if we hold 'w' then the cobject will only go up and never come down
    self.attacking = False
    self.update_time = pygame.time.get_ticks() #Measures the time from when the fighter gets created
    self.attack_type = 0
    self.health = 100
    self.attack_cooldown = 0
    # self.attack_sound = sound
    self.hit = False
    self.health = 100
    self.alive = True
    self.running = False
    self.update_action=0

  def load_images(self, sprite_sheet, animation_steps):
    #extract images from spritesheet
    animation_list = []
    for y, animation in enumerate(animation_steps):
      temp_img_list = []
      for x in range(animation):
        temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
        temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
      animation_list.append(temp_img_list)
    return animation_list

  # def move(self, screen_width, screen_height, surface, target, round_over):
  def move(self, screen_width, screen_height,surface,target):
    SPEED = 10 #speed at which the fighter object moves in the screen
    GRAVITY = 2 # without this the player jumps , it goes totally up and out of the screen
    dx = 0 #change in x coordinate. dx and dy = 0 means initially the player is stationary
    dy = 0 #change in y coordinate
    # self.running = False
    # self.attack_type = 0

    # get keypresses
    key = pygame.key.get_pressed() # First step for assigning keys for movement

    # movement
    #left movement -> a, right movement -> d, up_movement(jump) -> w, down_movement(jump) -> s
    if key[pygame.K_a]: # pygame.K_(button need to be pressed) -> that's how it needs to written. It will get started when the button 'a' is pressed.
      dx = -SPEED #when object moves left the 'dx' value becomes negative , since the 'x' coordinate will decrease
      self.running = True
    if key[pygame.K_d]:
      dx = SPEED  #when object moves right the 'dx' value becomes positive , since the 'x' coordinate will increase
      self.running = True

    # jump
    if key[pygame.K_w] and self.jump == False : # I am using self.jump == False to avoid continuous jump or double jump.So as long was we are not jumping , we can press the 'w' key
        self.vel_y = -30  #It will jump upto 30 coordinate
        self.jump = True # After we jumped the 'self.jump' needs to be set back to true

    # attack
    if key[pygame.K_r] or key[pygame.K_t]: # 'r' and 't' keys are used for attacks
        # self.attack(target)
        self.attack(surface,target)
        # determine which attack type was used
        if key[pygame.K_r]:
          self.attack_type = 1
        if key[pygame.K_t]:
          self.attack_type = 2


    # apply gravity
    self.vel_y += GRAVITY # The 'y' velocity is always brought back down byt the GRAVITY variable.Until this, if we run, the boxes will just directly fall off the screen.
    dy += self.vel_y

    # ensure player stays on screen
    if self.rect.left + dx < 0:
        dx = -self.rect.left
    if self.rect.right + dx > screen_width:
        dx = screen_width - self.rect.right
    if self.rect.bottom + dy > screen_height - 110:
      self.vel_y = 0
      self.jump = False # If we don't use this, after pressing 'w' once the player is jumping, but next if we press 'w' again, the player won't jump. So we need this command here.
      dy = screen_height - 110 - self.rect.bottom

    # ensure players face each other
    if target.rect.centerx > self.rect.centerx: # If target is on the right hand side of the player , we don't need to flip, otherwise we need to flip
        self.flip = False
    else:
        self.flip = True

    # update player position
    self.rect.x += dx
    self.rect.y += dy

  # handle animation updates
  def update(self):
      # check what action the player is performing
      if self.health <= 0:
        self.health = 0
        self.alive = False
        self.update_action=6  # 6:death
      elif self.hit == True:
        self.update_action=5  # 5:hit
      elif self.attacking == True:
        if self.attack_type == 1:
          self.update_action=3  # 3:attack1
        elif self.attack_type == 2:
          self.update_action=4  # 4:attack2
      elif self.jump == True:
        self.update_action=2  # 2:jump
      elif self.running == True:
        self.update_action=1  # 1:run
      else:
        self.update_action=0  # 0:idle

      animation_cooldown = 50 #each animation frame is going to take 50 millisecond
      # update image
      self.image = self.animation_list[self.action][self.frame_index]
      # check if enough time has passed since the last update
      if pygame.time.get_ticks() - self.update_time > animation_cooldown:
        self.frame_index += 1
        self.update_time = pygame.time.get_ticks()
      # check if the animation has finished
      if self.frame_index >= len(self.animation_list[self.action]):
        # if the player is dead then end the animation
        if self.alive == False:
          self.frame_index = len(self.animation_list[self.action]) - 1
        else:
          self.frame_index = 0
          # check if an attack was executed
          if self.action == 3 or self.action == 4:
            self.attacking = False
            self.attack_cooldown = 20
          # check if damage was taken
          if self.action == 5:
            self.hit = False
            # if the player was in the middle of an attack, then the attack is stopped
            self.attacking = False
            self.attack_cooldown = 20


  #We need to know when an attack is thrown and when it hit the enemy. as of now if we press 'r' and 't', they are getting registrered in the background but nothing will be shown in the screen.
  #For this one we need to predict if an opponent is close enough to get hit. so we need to create an attacking rectangle, which will get created in front of the opponent everytime it attacks. It will check whether the enemy and attacking rectangle are colliding.
  def attack(self,surface, target):
    # if self.attack_cooldown == 0:
      # execute attack
      self.attacking = True
      # self.attack_sound.play()
      attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height) # When player is on left side of target, the term self.flip = false, so the term (2 * self.rect.width * self.flip)=0, but when the player is on the right hand side of the target, it needs to flip, then the attacking reactangle has to be on the opposite side as well
      if attacking_rect.colliderect(target.rect):
        target.health -= 10
        target.hit = True

  def draw(self, surface):
    img = pygame.transform.flip(self.image, self.flip, False)
    surface.blit(img,(self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))