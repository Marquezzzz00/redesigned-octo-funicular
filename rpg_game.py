import random
from enum import Enum
from typing import List, Optional

class CharacterClass(Enum):
    """Classes disponíveis no jogo"""
    WARRIOR = "Guerreiro"
    MAGE = "Mago"
    ARCHER = "Arqueiro"
    PALADIN = "Paladino"

class Item:
    """Representa um item no jogo"""
    def __init__(self, name: str, item_type: str, value: int):
        self.name = name
        self.item_type = item_type  # 'weapon', 'armor', 'potion'
        self.value = value
    
    def __str__(self):
        return f"{self.name} (+{self.value})"

class Character:
    """Classe base para personagens"""
    def __init__(self, name: str, char_class: CharacterClass):
        self.name = name
        self.char_class = char_class
        self.level = 1
        self.experience = 0
        self.experience_to_level = 100
        
        # Stats base
        self.max_hp = 100
        self.current_hp = self.max_hp
        self.mana = 50
        self.max_mana = 50
        self.attack = 10
        self.defense = 5
        self.magic = 8
        
        # Ajustes por classe
        self._setup_class_stats()
        
        self.inventory: List[Item] = []
        self.equipped_weapon: Optional[Item] = None
        self.equipped_armor: Optional[Item] = None
    
    def _setup_class_stats(self):
        """Ajusta stats baseado na classe do personagem"""
        if self.char_class == CharacterClass.WARRIOR:
            self.max_hp = 150
            self.attack = 15
            self.defense = 12
        elif self.char_class == CharacterClass.MAGE:
            self.max_mana = 100
            self.magic = 20
            self.attack = 6
            self.max_hp = 80
        elif self.char_class == CharacterClass.ARCHER:
            self.attack = 18
            self.max_hp = 110
        elif self.char_class == CharacterClass.PALADIN:
            self.max_hp = 130
            self.attack = 12
            self.defense = 15
            self.max_mana = 60
        
        self.current_hp = self.max_hp
        self.mana = self.max_mana
    
    def take_damage(self, damage: int) -> int:
        """Recebe dano, considerando defesa"""
        actual_damage = max(1, damage - self.defense // 2)
        self.current_hp -= actual_damage
        return actual_damage
    
    def heal(self, amount: int) -> int:
        """Cura o personagem"""
        healed = min(amount, self.max_hp - self.current_hp)
        self.current_hp += healed
        return healed
    
    def use_mana(self, amount: int) -> bool:
        """Tenta usar mana"""
        if self.mana >= amount:
            self.mana -= amount
            return True
        return False
    
    def restore_mana(self, amount: int):
        """Restaura mana"""
        self.mana = min(self.mana + amount, self.max_mana)
    
    def add_experience(self, amount: int):
        """Adiciona experiência e checa se sobe de nível"""
        self.experience += amount
        while self.experience >= self.experience_to_level:
            self.level_up()
    
    def level_up(self):
        """Sobe de nível"""
        self.level += 1
        self.experience -= self.experience_to_level
        self.experience_to_level = int(self.experience_to_level * 1.1)
        
        # Aumenta stats
        self.max_hp = int(self.max_hp * 1.1)
        self.current_hp = self.max_hp
        self.attack = int(self.attack * 1.1)
        self.defense = int(self.defense * 1.1)
        self.magic = int(self.magic * 1.1)
        self.max_mana = int(self.max_mana * 1.1)
        self.mana = self.max_mana
    
    def equip_item(self, item: Item) -> bool:
        """Equipa um item do inventário"""
        if item not in self.inventory:
            return False
        
        if item.item_type == 'weapon':
            self.equipped_weapon = item
            return True
        elif item.item_type == 'armor':
            self.equipped_armor = item
            return True
        return False
    
    def get_attack_power(self) -> int:
        """Calcula poder de ataque total"""
        power = self.attack
        if self.equipped_weapon:
            power += self.equipped_weapon.value
        return power
    
    def get_defense_power(self) -> int:
        """Calcula poder de defesa total"""
        power = self.defense
        if self.equipped_armor:
            power += self.equipped_armor.value
        return power
    
    def is_alive(self) -> bool:
        """Verifica se o personagem está vivo"""
        return self.current_hp > 0
    
    def show_status(self) -> str:
        """Exibe status do personagem"""
        weapon_str = f" ({self.equipped_weapon.name})" if self.equipped_weapon else ""
        armor_str = f" ({self.equipped_armor.name})" if self.equipped_armor else ""
        
        status = f"""
╔════════════════════════════════════╗
║ {self.name} - Nível {self.level}
║ Classe: {self.char_class.value}
╠════════════════════════════════════╣
║ HP: {self.current_hp}/{self.max_hp}
║ Mana: {self.mana}/{self.max_mana}
║ XP: {self.experience}/{self.experience_to_level}
╠════════════════════════════════════╣
║ Ataque: {self.get_attack_power()}{weapon_str}
║ Defesa: {self.get_defense_power()}{armor_str}
║ Magia: {self.magic}
║ Itens no inventário: {len(self.inventory)}
╚════════════════════════════════════╝
"""
        return status

class Enemy:
    """Representa um inimigo"""
    def __init__(self, name: str, level: int, hp: int, attack: int, defense: int):
        self.name = name
        self.level = level
        self.max_hp = hp
        self.current_hp = hp
        self.attack = attack
        self.defense = defense
        self.experience_reward = level * 25
    
    def take_damage(self, damage: int) -> int:
        """Recebe dano"""
        actual_damage = max(1, damage - self.defense // 2)
        self.current_hp -= actual_damage
        return actual_damage
    
    def is_alive(self) -> bool:
        """Verifica se está vivo"""
        return self.current_hp > 0
    
    def get_attack_power(self) -> int:
        """Retorna poder de ataque"""
        return self.attack + random.randint(1, 5)

class Combat:
    """Sistema de combate"""
    def __init__(self, player: Character, enemy: Enemy):
        self.player = player
        self.enemy = enemy
        self.turn = 0
        self.log: List[str] = []
    
    def add_log(self, message: str):
        """Adiciona mensagem ao log"""
        self.log.append(message)
        print(message)
    
    def player_attack(self) -> bool:
        """Ataque do jogador"""
        damage = self.player.get_attack_power() + random.randint(1, 10)
        actual_damage = self.enemy.take_damage(damage)
        
        self.add_log(f"\n⚔️  {self.player.name} ataca! Dano: {actual_damage}")
        
        if not self.enemy.is_alive():
            self.add_log(f"💀 {self.enemy.name} foi derrotado!")
            return False
        
        self.add_log(f"❤️  {self.enemy.name} tem {self.enemy.current_hp} HP restantes")
        return True
    
    def player_cast_spell(self, spell: str = "fireball") -> bool:
        """Usa magia"""
        spells = {
            "fireball": {"cost": 20, "damage": 30, "name": "Bola de Fogo"},
            "heal": {"cost": 15, "healing": 40, "name": "Cura"},
            "lightning": {"cost": 25, "damage": 40, "name": "Relâmpago"}
        }
        
        if spell not in spells:
            self.add_log("Magia desconhecida!")
            return True
        
        spell_info = spells[spell]
        
        if not self.player.use_mana(spell_info["cost"]):
            self.add_log(f"❌ Mana insuficiente! (Necessário: {spell_info['cost']}, Atual: {self.player.mana})")
            return True
        
        if "damage" in spell_info:
            damage = spell_info["damage"] + random.randint(1, 10)
            actual_damage = self.enemy.take_damage(damage)
            self.add_log(f"✨ {self.player.name} lança {spell_info['name']}! Dano: {actual_damage}")
            
            if not self.enemy.is_alive():
                self.add_log(f"💀 {self.enemy.name} foi derrotado!")
                return False
        else:
            healed = self.player.heal(spell_info["healing"])
            self.add_log(f"✨ {self.player.name} lança {spell_info['name']}! Recuperados: {healed} HP")
        
        return True
    
    def player_defend(self) -> bool:
        """Defesa aumentada do jogador"""
        self.player.defense += 5
        self.add_log(f"🛡️  {self.player.name} se defende! Defesa +5")
        return True
    
    def enemy_turn(self) -> bool:
        """Turno do inimigo"""
        damage = self.enemy.get_attack_power()
        actual_damage = self.player.take_damage(damage)
        
        self.add_log(f"\n⚔️  {self.enemy.name} ataca! Dano: {actual_damage}")
        
        if not self.player.is_alive():
            self.add_log(f"💀 {self.player.name} foi derrotado!")
            return False
        
        self.add_log(f"❤️  {self.player.name} tem {self.player.current_hp} HP restantes")
        return True
    
    def start_combat(self):
        """Inicia o combate interativo"""
        self.add_log(f"\n{'='*50}")
        self.add_log(f"🎭 Combate iniciado contra {self.enemy.name}!")
        self.add_log(f"{'='*50}\n")
        
        while self.player.is_alive() and self.enemy.is_alive():
            self.turn += 1
            self.add_log(f"\n--- TURNO {self.turn} ---")
            self.add_log(f"🔴 Seu HP: {self.player.current_hp}/{self.player.max_hp}")
            self.add_log(f"⚫ HP do inimigo: {self.enemy.current_hp}/{self.enemy.max_hp}\n")
            
            # Menu de ações
            valid_choice = False
            while not valid_choice:
                print("Escolha uma ação:")
                print("1. Atacar")
                print("2. Lançar magia")
                print("3. Defender")
                print("4. Ver status")
                
                choice = input("\nSua escolha (1-4): ").strip()
                
                if choice == "1":
                    valid_choice = self.player_attack()
                elif choice == "2":
                    print("\nMagias disponíveis:")
                    print("1. Fireball (custo: 20 mana, dano: 30)")
                    print("2. Heal (custo: 15 mana, cura: 40)")
                    print("3. Lightning (custo: 25 mana, dano: 40)")
                    spell_choice = input("Escolha a magia (1-3): ").strip()
                    
                    spell_map = {"1": "fireball", "2": "heal", "3": "lightning"}
                    if spell_choice in spell_map:
                        valid_choice = self.player_cast_spell(spell_map[spell_choice])
                    else:
                        print("Opção inválida!")
                        continue
                elif choice == "3":
                    valid_choice = self.player_defend()
                elif choice == "4":
                    print(self.player.show_status())
                    continue
                else:
                    print("Opção inválida!")
                    continue
            
            if not self.enemy.is_alive():
                break
            
            # Turno do inimigo
            if not self.enemy_turn():
                break
        
        # Resultado final
        self.add_log(f"\n{'='*50}")
        if self.player.is_alive():
            self.add_log("🏆 VITÓRIA!")
            self.player.add_experience(self.enemy.experience_reward)
            self.add_log(f"⭐ Ganhou {self.enemy.experience_reward} XP!")
        else:
            self.add_log("☠️  DERROTA!")
        self.add_log(f"{'='*50}\n")

class Game:
    """Classe principal do jogo"""
    def __init__(self):
        self.player: Optional[Character] = None
        self.enemies = [
            Enemy("Goblin", 1, 30, 8, 2),
            Enemy("Orc", 2, 50, 12, 4),
            Enemy("Dragão", 5, 200, 25, 10),
            Enemy("Skeleton", 2, 40, 10, 3),
        ]
    
    def create_character(self):
        """Cria um novo personagem"""
        print("\n╔════════════════════════════════════╗")
        print("║   BEM-VINDO AO RPG AVENTURA!      ║")
        print("╚════════════════════════════════════╝\n")
        
        name = input("Digite o nome do seu personagem: ").strip()
        
        print("\nEscolha sua classe:")
        print("1. Guerreiro (HP Alto, Ataque Forte)")
        print("2. Mago (Mana Alta, Magia Forte)")
        print("3. Arqueiro (Ataque Rápido)")
        print("4. Paladino (Balanceado, Defesa Boa)")
        
        class_choice = input("\nSua escolha (1-4): ").strip()
        
        class_map = {
            "1": CharacterClass.WARRIOR,
            "2": CharacterClass.MAGE,
            "3": CharacterClass.ARCHER,
            "4": CharacterClass.PALADIN
        }
        
        if class_choice not in class_map:
            print("Opção inválida! Guerreiro selecionado por padrão.")
            char_class = CharacterClass.WARRIOR
        else:
            char_class = class_map[class_choice]
        
        self.player = Character(name, char_class)
        print(self.player.show_status())
    
    def main_menu(self):
        """Menu principal do jogo"""
        while True:
            print("\n╔════════════════════════════════════╗")
            print("║         MENU PRINCIPAL             ║")
            print("╠════════════════════════════════════╣")
            print("║ 1. Ver Status                      ║")
            print("║ 2. Explorar (Combate)              ║")
            print("║ 3. Ver Inventário                  ║")
            print("║ 4. Gerenciar Equipamento           ║")
            print("║ 5. Sair do Jogo                    ║")
            print("╚════════════════════════════════════╝")
            
            choice = input("\nSua escolha (1-5): ").strip()
            
            if choice == "1":
                print(self.player.show_status())
            elif choice == "2":
                self.explore()
            elif choice == "3":
                self.show_inventory()
            elif choice == "4":
                self.manage_equipment()
            elif choice == "5":
                print(f"\nObrigado por jogar! Até logo, {self.player.name}!")
                break
            else:
                print("Opção inválida!")
    
    def explore(self):
        """Sistema de exploração com combate"""
        if not self.player:
            print("Crie um personagem primeiro!")
            return
        
        print("\nVocê está explorando a floresta...\n")
        enemy = random.choice(self.enemies)
        enemy.current_hp = enemy.max_hp  # Reseta HP do inimigo
        
        print(f"Um {enemy.name} apareceu! (Nível: {enemy.level})\n")
        
        combat = Combat(self.player, enemy)
        combat.start_combat()
    
    def show_inventory(self):
        """Mostra o inventário do jogador"""
        if not self.player:
            print("Crie um personagem primeiro!")
            return
        
        print(f"\n📦 Inventário de {self.player.name}:")
        
        if not self.player.inventory:
            print("Inventário vazio!")
            return
        
        for i, item in enumerate(self.player.inventory, 1):
            equipped = ""
            if self.player.equipped_weapon == item:
                equipped = " [EQUIPADO - Arma]"
            elif self.player.equipped_armor == item:
                equipped = " [EQUIPADO - Armadura]"
            print(f"{i}. {item.name} ({item.item_type}) {equipped}")
    
    def manage_equipment(self):
        """Gerencia equipamento do jogador"""
        if not self.player:
            print("Crie um personagem primeiro!")
            return
        
        print("\nEquipamento Atual:")
        print(f"Arma: {self.player.equipped_weapon.name if self.player.equipped_weapon else 'Nenhuma'}")
        print(f"Armadura: {self.player.equipped_armor.name if self.player.equipped_armor else 'Nenhuma'}")
        
        if not self.player.inventory:
            print("\nInventário vazio!")
            return
        
        print("\nItens disponíveis:")
        for i, item in enumerate(self.player.inventory, 1):
            print(f"{i}. {item.name} ({item.item_type}) {item}")
        
        choice = input("\nEscolha um item para equipar (ou 0 para cancelar): ").strip()
        
        try:
            idx = int(choice) - 1
            if idx == -1:
                return
            if 0 <= idx < len(self.player.inventory):
                item = self.player.inventory[idx]
                if self.player.equip_item(item):
                    print(f"✓ {item.name} equipado!")
                else:
                    print("Tipo de item inválido!")
        except ValueError:
            print("Entrada inválida!")
    
    def run(self):
        """Executa o jogo"""
        self.create_character()
        self.main_menu()

def main():
    """Função principal"""
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
