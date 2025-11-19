# User

- id
- id_player
- id_tg
- phone
- is_real_phone
- is_active
- datetime_reg
- datetime_upd

# Player

- id
- name
- title
- avatar
- level
- xp
- lp
- hp
- max_hp
- mp
- max_mp
- weight
- max_weight
- base_damage
- base_armor
- money
- karma
- state
- last_action
- id_game_class
- is_active
- datetime_last

# GameClass

- id
- name
- description
- delta_attributes // json

# Levels

- level
- target_xp
- reward_lp

# Parameter

- id
- name
- description
- symbol
- cost_lp
- minimal_level
- maximum_power
- required_classes // array
- impact_per_level // json

# PlayerParameter

- id
- id_player
- id_parameter
- power

# Location

- id
- name
- description
- image
- type

# Item

- id
- name
- description
- image
- weight
- cost
- rare // enum( 'Обычный', 'Необычный', 'Редкий', 'Эпический', 'Легендарный', 'Мифический', 'Секретный' )
- type // enum( 'Оружие', 'Щит', 'Еда', 'Броня', 'Зелье', 'Предмет'  )
- attributes // json

# Inventory

- id
- id_player
- id_item
- quantity
- is_equpped

# Enemy

- id
- name
- description
- image
- level
- hp
- mp
- damage
- armor
- reward_xp
- reward_money
- state
- last_action
- loot // json

# LocationEnemy

- id
- location_id
- enemy_id
- spawn_chance

# Effect

- id
- name
- description
- symbol
- image
- type // enum(положительный, отрицательный, нейтральный)
- duration
- impact // json

# PlayerEffect

- id
- id_player
- id_effect
- duration_remaining

# LocationEffect

- id
- id_location
- id_effect
- duration_remaining
- is_infinity

# Skill

- id
- name
- description
- required_level
- required_classes // array
- cooldown
- attributes // json

# Battle:

- id
- id_player
- id_enemy
- current_turn
- state // enum(начало, в процессе, завершен)
- created_at
- updated_at
