import os, sys
import pygame

#A colisão em Y é desconsiderada
#A ordem é (Quem irá se mover | Quem será o alvo do teste de colisão)
#colisionMobPlayer => O mob colidiu com o player?

"""
Todos os metodos foram simplesmente movidos para cá, necessario alterar quando tiver tempo
"""

class Colision:
    def __init__(self):
        pass

    @staticmethod
    def colisionMobPlayer(player, mob):
        tempMobRect = mob.getRectMob().copy()
        tempMobRect.y = mob.player.getRectPlayer().y
        if player.getRectPlayer().colliderect(tempMobRect):
            return True
        if tempMobRect.colliderect(player.getRectPlayer()):
            return True
        return False

    #Slime
    @staticmethod
    def colisionSlimePlayer(player, mob, dif):
        tempMobRect = mob.getRectMob().copy()
        if mob.mobVelocity > 0:
            tempMobRect.x += dif
        else:
            tempMobRect.x -= dif
        tempMobRect.y = player.getRectPlayer().y
        if player.getRectPlayer().colliderect(tempMobRect):
            return True
        if tempMobRect.colliderect(player.getRectPlayer()):
            return True
        return False

    @staticmethod
    def colisionSlimeAttackPlayer(player, mob):
        if player.inJump:                   #Se está pulando não faz a checagem de colisão
            player.removeColision()    	  #Remove as colisoes
            return

        tempMobRect = mob.getRectMobAttack1().copy()
        tempMobRect.y = player.getRectPlayer().y
        if player.getRectPlayer().colliderect(tempMobRect):
            player.setDamage(mob.slimeAttack0Damage)
        elif tempMobRect.colliderect(player.getRectPlayer()):
            player.setDamage(mob.slimeAttack0Damage)

    @staticmethod
    def colisionPlayerMob(player, mob):
        if player.inJump:                   #Se está pulando não faz a checagem de colisão
            player.removeColision()    	  #Remove as colisoes
            return

        tempMobRect = mob.getRectMob().copy()
        tempMobRect.y = player.getRectPlayer().y
        if mob.mobVelocity > 0:
            if player.getRectPlayer().colliderect(tempMobRect):                #Verifica a colisão entre o player e o rect
                player.setDamage(mob.mobDamage)
                player.colisionLeft = True
            else:
                player.colisionLeft = False
        elif mob.mobVelocity < 0:
            if tempMobRect.colliderect(player.getRectPlayer()):                #Verifica a colisão entre o mod e o player
                player.setDamage(mob.mobDamage)
                player.colisionRight = True
            else:
                player.colisionRight = False

    @staticmethod
    def colisionPlayerMoney(player, money):
        tempRect = money.getMoneyRect().copy()
        tempRect.x = money.posXDrop
        tempRect.y = player.getRectPlayer().y

        if tempRect.colliderect(player.getRectPlayer()):
            return True
        if player.getRectPlayer().colliderect(tempRect):
            return True
        return False

    @staticmethod
    def colisionPlayerNPC(player, npc):
        tempRect = npc.getRectNPC().copy()
        tempRect.y = player.getRectPlayer().y  #Ignora a posY
        if tempRect.colliderect(player.getRectPlayer()):
            npc.colisionPlayer = True
        elif player.getRectPlayer().colliderect(tempRect):
            npc.colisionPlayer = True
        else:
            npc.colisionPlayer = False
            

    @staticmethod
    def colisionWeaponMob(weapon, mob):
        if not weapon.inAttack():
            return
        tempRectWeapon = weapon.getRectWeapon()
        tempRectWeapon.y = mob.getRectMob().y
        if tempRectWeapon.colliderect(mob.getRectMob()):
            mob.setDamage()
        elif mob.getRectMob().colliderect(tempRectWeapon):
            mob.setDamage()