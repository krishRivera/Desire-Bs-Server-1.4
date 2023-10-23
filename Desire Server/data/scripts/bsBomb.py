import bs
import bsUtils
import bdUtils
from bsVector import Vector
import random
import portalObjects
import weakref
from bsSpaz import SleepMessage,ToxicMessage
import hack

class BombFactory(object):
    """
    category: Game Flow Classes

    Wraps up media and other resources used by bs.Bombs
    A single instance of this is shared between all bombs
    and can be retrieved via bs.Bomb.getFactory().

    Attributes:

       bombModel
          The bs.Model of a standard or ice bomb.

       stickyBombModel
          The bs.Model of a sticky-bomb.

       impactBombModel
          The bs.Model of an impact-bomb.

       landMinModel
          The bs.Model of a land-mine.

       tntModel
          The bs.Model of a tnt box.

       regularTex
          The bs.Texture for regular bombs.

       iceTex
          The bs.Texture for ice bombs.

       stickyTex
          The bs.Texture for sticky bombs.

       impactTex
          The bs.Texture for impact bombs.

       impactLitTex
          The bs.Texture for impact bombs with lights lit.

       landMineTex
          The bs.Texture for land-mines.

       landMineLitTex
          The bs.Texture for land-mines with the light lit.

       tntTex
          The bs.Texture for tnt boxes.

       hissSound
          The bs.Sound for the hiss sound an ice bomb makes.

       debrisFallSound
          The bs.Sound for random falling debris after an explosion.

       woodDebrisFallSound
          A bs.Sound for random wood debris falling after an explosion.

       explodeSounds
          A tuple of bs.Sounds for explosions.

       freezeSound
          A bs.Sound of an ice bomb freezing something.

       fuseSound
          A bs.Sound of a burning fuse.

       activateSound
          A bs.Sound for an activating impact bomb.

       warnSound
          A bs.Sound for an impact bomb about to explode due to time-out.

       bombMaterial
          A bs.Material applied to all bombs.

       normalSoundMaterial
          A bs.Material that generates standard bomb noises on impacts, etc.

       stickyMaterial
          A bs.Material that makes 'splat' sounds and makes collisions softer.

       landMineNoExplodeMaterial
          A bs.Material that keeps land-mines from blowing up.
          Applied to land-mines when they are created to allow land-mines to
          touch without exploding.

       landMineBlastMaterial
          A bs.Material applied to activated land-mines that causes them to
          explode on impact.

       impactBlastMaterial
          A bs.Material applied to activated impact-bombs that causes them to
          explode on impact.

       blastMaterial
          A bs.Material applied to bomb blast geometry which triggers impact
          events with what it touches.

       dinkSounds
          A tuple of bs.Sounds for when bombs hit the ground.

       stickyImpactSound
          The bs.Sound for a squish made by a sticky bomb hitting something.

       rollSound
          bs.Sound for a rolling bomb.
    """

    def getRandomExplodeSound(self):
        'Return a random explosion bs.Sound from the factory.'
        return self.explodeSounds[random.randrange(len(self.explodeSounds))]

    def __init__(self):
        """
        Instantiate a BombFactory.
        You shouldn't need to do this; call bs.Bomb.getFactory() to get a
        shared instance.
        """

        self.bombModel = bs.getModel('bomb')
        self.stickyBombModel = bs.getModel('bombSticky')
        self.impactBombModel = bs.getModel('impactBomb')
        self.bananaModel = bs.getModel("impactBomb")
        self.landMineModel = bs.getModel('landMine')
        self.sleepPotionModel = bs.getModel('bomb')
        self.shockWaveModel = bs.getModel("impactBomb")
        self.enderPearlModel = bs.getModel('bomb')
        self.curseBombModel = bs.getModel('bonesHead')
        self.elonMineModel = bs.getModel('landMine')
        self.weedbombModel = bs.getModel('frostyHead')
        self.tntModel = bs.getModel('tnt')

        self.regularTex = bs.getTexture('bombColor')
        self.iceTex = bs.getTexture('bombColorIce')
        self.stickyTex = bs.getTexture('bombStickyColor')
        self.forceTex = bs.getTexture('egg2')
        self.impactTex = bs.getTexture('impactBombColor')
        self.impactLitTex = bs.getTexture('impactBombColorLit')
        self.enderPearlTex = bs.getTexture('crossOutMask')
        self.radioactiveTex = bs.getTexture('powerupStickyBombs')
        self.sleepPotionTex = bs.getTexture('powerupShield')
        self.bananaTex = bs.getTexture("bombStickyColor")
        self.shockWaveTex = bs.getTexture("rgbStripes")
        self.curseBombTex = bs.getTexture('powerupCurse')
        self.landMineTex = bs.getTexture('landMine')
        self.landMineLitTex = bs.getTexture('landMineLit')
        self.elonMineTex = bs.getTexture('achievementCrossHair')
        self.elonMineLitTex = bs.getTexture('achievementMine')
        self.weedbombTex = bs.getTexture('egg3')
        self.tntTex = bs.getTexture('tnt')

        self.hissSound = bs.getSound('hiss')
        self.debrisFallSound = bs.getSound('debrisFall')
        self.enderPearlExplodeSound = bs.getSound('activateBeep')
        self.woodDebrisFallSound = bs.getSound('woodDebrisFall')
        self.sleepPotionExplodeSound = bs.getSound('explosion01')

        self.explodeSounds = (bs.getSound('explosion01'),
                              bs.getSound('explosion02'),
                              bs.getSound('explosion03'),
                              bs.getSound('explosion04'),
                              bs.getSound('explosion05'))

        self.freezeSound = bs.getSound('freeze')
        self.fuseSound = bs.getSound('fuse01')
        self.shockWaveSound = bs.getSound("fuse01")
        self.activateSound = bs.getSound('activateBeep')
        self.warnSound = bs.getSound('warnBeep')

        # set up our material so new bombs dont collide with objects
        # that they are initially overlapping
        self.bombMaterial = bs.Material()
        self.normalSoundMaterial = bs.Material()
        self.stickyMaterial = bs.Material()

        self.bombMaterial.addActions(
            conditions=((('weAreYoungerThan',100),
                         'or',('theyAreYoungerThan',100)),
                        'and',('theyHaveMaterial',
                               bs.getSharedObject('objectMaterial'))),
            actions=(('modifyNodeCollision','collide',False)))

        # we want pickup materials to always hit us even if we're currently not
        # colliding with their node (generally due to the above rule)
        self.bombMaterial.addActions(
            conditions=('theyHaveMaterial',
                        bs.getSharedObject('pickupMaterial')),
            actions=(('modifyPartCollision','useNodeCollide', False)))
        
        self.bombMaterial.addActions(actions=('modifyPartCollision',
                                              'friction', 0.3))

        self.landMineNoExplodeMaterial = bs.Material()
        self.landMineBlastMaterial = bs.Material()
        self.landMineBlastMaterial.addActions(
            conditions=(
                ('weAreOlderThan',200),
                 'and', ('theyAreOlderThan',200),
                 'and', ('evalColliding',),
                 'and', (('theyDontHaveMaterial',
                          self.landMineNoExplodeMaterial),
                         'and', (('theyHaveMaterial',
                                  bs.getSharedObject('objectMaterial')),
                                 'or',('theyHaveMaterial',
                                       bs.getSharedObject('playerMaterial'))))),
            actions=(('message', 'ourNode', 'atConnect', ImpactMessage())))
        
        self.impactBlastMaterial = bs.Material()
        self.impactBlastMaterial.addActions(
            conditions=(('weAreOlderThan', 200),
                        'and', ('theyAreOlderThan',200),
                        'and', ('evalColliding',),
                        'and', (('theyHaveMaterial',
                                 bs.getSharedObject('footingMaterial')),
                               'or',('theyHaveMaterial',
                                     bs.getSharedObject('objectMaterial')))),
            actions=(('message','ourNode','atConnect',ImpactMessage())))

        self.blastMaterial = bs.Material()
        self.blastMaterial.addActions(
            conditions=(('theyHaveMaterial',
                         bs.getSharedObject('objectMaterial'))),
            actions=(('modifyPartCollision','collide',True),
                     ('modifyPartCollision','physical',False),
                     ('message','ourNode','atConnect',ExplodeHitMessage())))

        self.dinkSounds = (bs.getSound('bombDrop01'),
                           bs.getSound('bombDrop02'))
        self.stickyImpactSound = bs.getSound('stickyImpact')
        self.rollSound = bs.getSound('bombRoll01')

        # collision sounds
        self.normalSoundMaterial.addActions(
            conditions=('theyHaveMaterial',
                        bs.getSharedObject('footingMaterial')),
            actions=(('impactSound',self.dinkSounds,2,0.8),
                     ('rollSound',self.rollSound,3,6)))

        self.stickyMaterial.addActions(
            actions=(('modifyPartCollision','stiffness',0.1),
                     ('modifyPartCollision','damping',1.0)))

        self.stickyMaterial.addActions(
            conditions=(('theyHaveMaterial',
                         bs.getSharedObject('playerMaterial')),
                        'or', ('theyHaveMaterial',
                               bs.getSharedObject('footingMaterial'))),
            actions=(('message','ourNode','atConnect',SplatMessage())))

class SplatMessage(object):
    pass

class ExplodeMessage(object):
    pass

class ImpactMessage(object):
    """ impact bomb touched something """
    pass

class SetStickyMessage(object):
    pass


class ArmMessage(object):
    pass

class WarnMessage(object):
    pass

class ExplodeHitMessage(object):
    "Message saying an object was hit"
    def __init__(self):
        pass

class Blast(bs.Actor):
    """
    category: Game Flow Classes

    An explosion, as generated by a bs.Bomb.
    """
    def __init__(self, position=(0,1,0), velocity=(0,0,0), blastRadius=2.0,
                 blastType="normal", sourcePlayer=None, hitType='explosion',
                 hitSubType='normal'):
        """
        Instantiate with given values.
        """
        bs.Actor.__init__(self)
        
        factory = Bomb.getFactory()

        self.blastType = blastType
        self.sourcePlayer = sourcePlayer

        self.hitType = hitType;
        self.hitSubType = hitSubType;

        # blast radius
        self.radius = blastRadius

        # set our position a bit lower so we throw more things upward
        self.node = bs.newNode('region', delegate=self, attrs={
            'position':(position[0], position[1]-0.1, position[2]),
            'scale':(self.radius,self.radius,self.radius),
            'type':'sphere',
            'materials':(factory.blastMaterial,
                         bs.getSharedObject('attackMaterial'))})

        bs.gameTimer(50, self.node.delete)

        # throw in an explosion and flash
        explosion = bs.newNode("explosion", attrs={
            'position':position,
            'velocity':(velocity[0],max(-1.0,velocity[1]),velocity[2]),
            'radius':self.radius,
            'big':(self.blastType == 'tnt')})
        if self.blastType == "ice":
            explosion.color = (0, 0.05, 0.4)
        elif self.blastType == "enderPearl":
            explosion.color = (0.6,0.3,0.3)
        elif self.blastType == "sleepPotion":
            explosion.color = (0.6,0,0.6)
        elif self.blastType == "toxic":
            explosion.color = (0,0.9,0)
        elif self.blastType == 'banana':
            explosion.color = (1, 1, 0)
        elif self.blastType == 'shockWave':
            explosion.color = (0.3, 0.3, 1)            

        bs.gameTimer(1000,explosion.delete)

        if self.blastType != 'ice':
            bs.emitBGDynamics(position=position, velocity=velocity,
                              count=int(1.0+random.random()*4),
                              emitType='tendrils',tendrilType='thinSmoke')
        if self.blastType != 'sleepPotion':
            bs.emitBGDynamics(
              position=position,velocity=velocity,
              count=int(4.0+random.random()*4),
              emitType='tendrils',tendrilType='ice' if self.blastType == 'ice' else 'smoke')
        bs.emitBGDynamics(
            position=position, emitType='distortion',
            spread=1.0 if self.blastType == 'tnt' else 2.0)
        
        # and emit some shrapnel..
        if self.blastType == 'ice':
            def _doEmit():    
                try:
                    bs.emitBGDynamics(position=(position[0]-1+random.random()*2,position[1]+random.random(),position[2]-1+random.random()*2),velocity=(0,0,0),count=5,scale=3.5,chunkType='ice',emitType='stickers');
                    bs.emitBGDynamics(position=(position[0]-1+random.random()*2,position[1]+random.random(),position[2]-1+random.random()*2),velocity=(0,0,0),count=5,scale=3.5,chunkType='ice',emitType='stickers');
                    bs.emitBGDynamics(position=(position[0]-1+random.random()*2,position[1]+random.random(),position[2]-1+random.random()*2),velocity=(0,0,0),count=5,scale=3.5,chunkType='ice',emitType='stickers');
                    bs.emitBGDynamics(position=(position[0]-1+random.random()*2,position[1]+random.random(),position[2]-1+random.random()*2),velocity=(0,0,0),count=5,scale=3.5,chunkType='ice',emitType='stickers');
                    bs.emitBGDynamics(position=(position[0]-1+random.random()*2,position[1]+random.random(),position[2]-1+random.random()*2),velocity=(0,0,0),count=5,scale=3.5,chunkType='ice',emitType='stickers');
                    bs.emitBGDynamics(position=(position[0]-1+random.random()*2,position[1]+random.random(),position[2]-1+random.random()*2),velocity=(0,0,0),count=5,scale=3.5,chunkType='ice',emitType='stickers');
                    bs.emitBGDynamics(position=(position[0]-1+random.random()*2,position[1]+random.random(),position[2]-1+random.random()*2),velocity=(0,0,0),count=5,scale=3.5,chunkType='ice',emitType='stickers');
                    bs.emitBGDynamics(position=(position[0]-1+random.random()*2,position[1]+random.random(),position[2]-1+random.random()*2),velocity=(0,0,0),count=5,scale=3.5,chunkType='ice',emitType='stickers');
                    bs.emitBGDynamics(position=(position[0]-1+random.random()*2,position[1]+random.random(),position[2]-1+random.random()*2),velocity=(0,0,0),count=5,scale=3.5,chunkType='ice',emitType='stickers');
                    bs.emitBGDynamics(position=(position[0]-1+random.random()*2,position[1]+random.random(),position[2]-1+random.random()*2),velocity=(0,0,0),count=5,scale=3.5,chunkType='ice',emitType='stickers');
                    bs.emitBGDynamics(position=(position[0]-1+random.random()*2,position[1]+random.random(),position[2]-1+random.random()*2),velocity=(0,0,0),count=5,scale=3.5,chunkType='ice',emitType='stickers');
                    bs.emitBGDynamics(position=(position[0]-1+random.random()*2,position[1]+random.random(),position[2]-1+random.random()*2),velocity=(0,0,0),count=5,scale=3.5,chunkType='ice',emitType='stickers');
                    #bs.emitBGDynamics(position=position,emitType='distortion',spread=6,count = 100);
                except:
                    pass
            bs.gameTimer(50,_doEmit) # looks better if we delay a bit

        elif self.blastType == 'banana':
            def _doEmit():
                for i in xrange(10):
                    bdUtils.Clay(
                        position=(position[0]-1+random.random()*2,
                                  position[1]+random.random(),
                                  position[2]-1+random.random()*2),
                        velocity=(-2+random.random()*4,
                                  -2+random.random()*4,
                                  -2+random.random()*4),
                        banana=True,
                        bomb=True).autoRetain()

                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=100,spread=0.5, scale=0.5, chunkType='spark')

            bs.gameTimer(15, _doEmit)

        elif self.blastType == 'enderPearl':
            def _doEmit():
                bs.emitBGDynamics(position=position,emitType='distortion',spread=0.2);
            bs.gameTimer(50,_doEmit) # looks better if we delay a bit
        elif self.blastType == 'sleepPotion':
            def _doEmit():
                bs.emitBGDynamics(position=position,emitType='distortion',spread=0.5);
                bs.emitBGDynamics(position=position,velocity=velocity,count=100,spread=0.5,scale=1.0,chunkType='spark');
            bs.gameTimer(50,_doEmit) # looks better if we delay a bit
        elif self.blastType == 'toxic':
            def _doEmit():
                bs.emitBGDynamics(position=position,velocity=velocity,count=int(6.0+random.random()*12),scale=0.8,spread=1.5,chunkType='spark');
            bs.gameTimer(50,_doEmit)

        elif self.blastType == 'sticky':
            def _doEmit():    
                try:
                    bs.emitBGDynamics(position=(position[0]-1+random.random()*2,position[1]+random.random(),position[2]-1+random.random()*2),velocity=(0,0,0),count=1,scale=3.5,chunkType='slime',emitType='stickers');
                    bs.emitBGDynamics(position=(position[0]-1+random.random()*2,position[1]+random.random(),position[2]-1+random.random()*2),velocity=(0,0,0),count=1,scale=3.5,chunkType='slime',emitType='stickers');
                    bs.emitBGDynamics(position=(position[0]-1+random.random()*2,position[1]+random.random(),position[2]-1+random.random()*2),velocity=(0,0,0),count=1,scale=3.5,chunkType='slime',emitType='stickers');
                    bs.emitBGDynamics(position=(position[0]-1+random.random()*2,position[1]+random.random(),position[2]-1+random.random()*2),velocity=(0,0,0),count=1,scale=3.5,chunkType='slime',emitType='stickers');
                    bs.emitBGDynamics(position=(position[0]-1+random.random()*2,position[1]+random.random(),position[2]-1+random.random()*2),velocity=(0,0,0),count=1,scale=3.5,chunkType='slime',emitType='stickers');
                    bs.emitBGDynamics(position=(position[0]-1+random.random()*2,position[1]+random.random(),position[2]-1+random.random()*2),velocity=(0,0,0),count=1,scale=3.5,chunkType='slime',emitType='stickers');
                    bs.emitBGDynamics(position=(position[0]-1+random.random()*2,position[1]+random.random(),position[2]-1+random.random()*2),velocity=(0,0,0),count=1,scale=3.5,chunkType='slime',emitType='stickers');
                    bs.emitBGDynamics(position=(position[0]-1+random.random()*2,position[1]+random.random(),position[2]-1+random.random()*2),velocity=(0,0,0),count=1,scale=3.5,chunkType='slime',emitType='stickers');
                    bs.emitBGDynamics(position=(position[0]-1+random.random()*2,position[1]+random.random(),position[2]-1+random.random()*2),velocity=(0,0,0),count=1,scale=3.5,chunkType='slime',emitType='stickers');
                    bs.emitBGDynamics(position=(position[0]-1+random.random()*2,position[1]+random.random(),position[2]-1+random.random()*2),velocity=(0,0,0),count=1,scale=3.5,chunkType='slime',emitType='stickers');
                    bs.emitBGDynamics(position=(position[0]-1+random.random()*2,position[1]+random.random(),position[2]-1+random.random()*2),velocity=(0,0,0),count=1,scale=3.5,chunkType='slime',emitType='stickers');
                    bs.emitBGDynamics(position=(position[0]-1+random.random()*2,position[1]+random.random(),position[2]-1+random.random()*2),velocity=(0,0,0),count=1,scale=3.5,chunkType='slime',emitType='stickers');
                    #bs.emitBGDynamics(position=position,emitType='distortion',spread=6,count = 100);
                except:
                    pass
            bs.gameTimer(50,_doEmit) # looks better if we delay a bit

        elif self.blastType == 'impact': # regular bomb shrapnel
            def _doEmit():
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0+random.random()*8), scale=0.8,
                                  chunkType='metal');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0+random.random()*8), scale=0.4,
                                  chunkType='metal');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=20, scale=0.7, chunkType='spark',
                                  emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(8.0+random.random()*15), scale=0.8,
                                  spread=1.5, chunkType='spark');
            bs.gameTimer(50,_doEmit) # looks better if we delay a bit

        elif self.blastType == 'curseBomb':  # regular bomb shrapnel
            def _doEmit():
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8), scale=0.8,
                                  chunkType='metal');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8), scale=0.4,
                                  chunkType='metal');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=20, scale=0.7, chunkType='spark',
                                  emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(8.0 + random.random() * 15), scale=0.8,
                                  spread=1.5, chunkType='spark');

            bs.gameTimer(50, _doEmit)  # looks better if we delay a bit
            
        elif self.blastType == 'shockWave':  # regular bomb shrapnel
            def _doEmit():
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8), scale=0.8,
                                  chunkType='metal');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8), scale=0.4,
                                  chunkType='metal');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=20, scale=0.7, chunkType='spark',
                                  emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(8.0 + random.random() * 15), scale=0.8,
                                  spread=1.5, chunkType='spark');

            bs.gameTimer(50, _doEmit)

        elif self.blastType == 'weedbomb':  # regular bomb shrapnel
            def _doEmit():
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8), scale=0.8,
                                  chunkType='metal');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8), scale=0.4,
                                  chunkType='metal');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=20, scale=0.7, chunkType='spark',
                                  emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(8.0 + random.random() * 15), scale=0.8,
                                  spread=1.5, chunkType='spark');

            bs.gameTimer(50, _doEmit)  # looks better if we delay a bit

        else: # regular or land mine bomb shrapnel
            def _doEmit():
                if self.blastType != 'tnt':
                    bs.emitBGDynamics(position=position, velocity=velocity,
                                      count=int(4.0+random.random()*8),
                                      chunkType='rock');
                    bs.emitBGDynamics(position=position, velocity=velocity,
                                      count=int(4.0+random.random()*8),
                                      scale=0.5,chunkType='rock');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=30,
                                  scale=1.0 if self.blastType=='tnt' else 0.7,
                                  chunkType='spark', emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(18.0+random.random()*20),
                                  scale=1.0 if self.blastType == 'tnt' else 0.8,
                                  spread=1.5, chunkType='spark');

                # tnt throws splintery chunks
                if self.blastType == 'tnt':
                    def _emitSplinters():
                        bs.emitBGDynamics(position=position, velocity=velocity,
                                          count=int(20.0+random.random()*25),
                                          scale=0.8, spread=1.0,
                                          chunkType='splinter');
                    bs.gameTimer(10,_emitSplinters)
                
                # every now and then do a sparky one
                if self.blastType == 'tnt' or random.random() < 0.1:
                    def _emitExtraSparks():
                        bs.emitBGDynamics(position=position, velocity=velocity,
                                          count=int(10.0+random.random()*20),
                                          scale=0.8, spread=1.5,
                                          chunkType='spark');
                    bs.gameTimer(20,_emitExtraSparks)
                        
            bs.gameTimer(50,_doEmit) # looks better if we delay a bit
        if self.blastType == 'banana':
            color = (1, 1, 0)

        light = bs.newNode('light', attrs={
            'position':position,
            'volumeIntensityScale': 10.0,
            'color': ((0.6, 0.6, 1.0) if self.blastType in ['ice','enderPearl']
                      else (1, 0.3, 0.1))})

        s = random.uniform(0.6,0.9)
        scorchRadius = lightRadius = self.radius
        if self.blastType == 'tnt':
            lightRadius *= 1.4
            scorchRadius *= 1.15
            s *= 3.0

        iScale = 1.6
        bsUtils.animate(light,"intensity", {
            0:2.0*iScale, int(s*20):0.1*iScale,
            int(s*25):0.2*iScale, int(s*50):17.0*iScale, int(s*60):5.0*iScale,
            int(s*80):4.0*iScale, int(s*200):0.6*iScale,
            int(s*2000):0.00*iScale, int(s*3000):0.0})
        bsUtils.animate(light,"radius", {
            0:lightRadius*0.2, int(s*50):lightRadius*0.55,
            int(s*100):lightRadius*0.3, int(s*300):lightRadius*0.15,
            int(s*1000):lightRadius*0.05})
        bs.gameTimer(int(s*3000),light.delete)

        # make a scorch that fades over time
        scorch = bs.newNode('scorch', attrs={
            'position':position,
            'size':scorchRadius*0.5,
            'big':(self.blastType == 'tnt')})
        if self.blastType == 'ice':
            scorch.color = (1,1,1.5)
        elif self.blastType == 'enderPearl':
            scorch.color = (0.6,0.3,0.3)
        elif self.blastType == 'sleepPotion':
            scorch.color = (0.7,0.6,0.7)
        elif self.blastType == 'banana':
                scorch.color = (1, 1, 0)

        bsUtils.animate(scorch,"presence",{3000:1, 13000:0})
        bs.gameTimer(13000,scorch.delete)

        if self.blastType == 'ice':
            bs.playSound(factory.hissSound,position=light.position)
            
        p = light.position
        if self.blastType == 'enderPearl':
            bs.playSound(factory.enderPearlExplodeSound,position=p)
        elif self.blastType == 'sleepPotion':
            bs.playSound(factory.sleepPotionExplodeSound,position=p)
        else:
            bs.playSound(factory.getRandomExplodeSound(),position=p)
            bs.playSound(factory.debrisFallSound,position=p)

        bs.shakeCamera(intensity=5.0 if self.blastType == 'tnt' else 1.0)

        # tnt is more epic..
        if self.blastType == 'tnt':
            bs.playSound(factory.getRandomExplodeSound(),position=p)
            def _extraBoom():
                bs.playSound(factory.getRandomExplodeSound(),position=p)
            bs.gameTimer(250,_extraBoom)
            def _extraDebrisSound():
                bs.playSound(factory.debrisFallSound,position=p)
                bs.playSound(factory.woodDebrisFallSound,position=p)
            bs.gameTimer(400,_extraDebrisSound)

    def handleMessage(self, msg):
        self._handleMessageSanityCheck()
        
        if isinstance(msg, bs.DieMessage):
            self.node.delete()

        elif isinstance(msg, ExplodeHitMessage):
            node = bs.getCollisionInfo("opposingNode")
            if node is not None and node.exists():
                t = self.node.position

                # new
                mag = 2000.0
                if self.blastType == 'ice': mag *= 0.5
                elif self.blastType == 'landMine': mag *= 2.5
                elif self.blastType == 'enderPearl': mag *= 0.1
                elif self.blastType == 'elonMine': mag *= 1.5
                elif self.blastType == 'forceBomb': mag *= 0.25
                elif self.blastType == 'sleepPotion': mag *= 0.1
                elif self.blastType == 'toxic': mag *= 0.5
                elif self.blastType == 'weedbomb': mag*= 0.5
                elif self.blastType == 'curseBomb': mag*= 0.0
                elif self.blastType == 'tnt': mag *= 2.0

                node.handleMessage(bs.HitMessage(
                    pos=t,
                    velocity=(0,0,0),
                    magnitude=mag,
                    hitType=self.hitType,
                    hitSubType=self.hitSubType,
                    radius=self.radius,
                    sourcePlayer=self.sourcePlayer))
                if self.blastType == "ice":
                    bs.playSound(Bomb.getFactory().freezeSound, 10, position=t)
                    node.handleMessage(bs.FreezeMessage())
                if self.blastType == "sleepPotion":
                    node.handleMessage(SleepMessage())
                if self.blastType == "toxic":
                    node.handleMessage(ToxicMessage())
                if self.blastType == "weedbomb" and not node.getNodeType() != 'spaz':
                    bs.playSound(Bomb.getFactory().hissSound, 9, position=t)#sobydamn
                    def weed():
                	    node.handleMessage("knockout",10000)
                    bs.gameTimer(2000,bs.Call(weed)) #delay (forgot about the epic)
                    bs.gameTimer(5500,bs.Call(weed))
                    bs.gameTimer(8500,bs.Call(weed))
                    def hiccups():
                    	bs.emitBGDynamics(position=(node.position[0],node.position[1]-1.2,node.position[2]), velocity=(0,0.05,0), count=random.randrange(100,270), scale=1+random.random(), spread=0.71, chunkType='sweat') #reminds me of tom and jerry
                    bs.gameTimer(1000,bs.Call(hiccups))
                    bs.gameTimer(2500,bs.Call(hiccups)) #showing we are alive
                    bs.gameTimer(5000,bs.Call(hiccups))
                    bs.gameTimer(7500,bs.Call(hiccups))
                    def look():
                    	bubble = bsUtils.PopupText("high",color=(1,1,1), scale=0.7, randomOffset=0.2, offset=(0,-1,0), position=(node.position[0],node.position[1]-1.2,node.position[2])).autoRetain()
                    bs.gameTimer(1500,bs.Call(look))
                    bs.gameTimer(3000,bs.Call(look))
                    bs.gameTimer(8000,bs.Call(look))
                    def look():
                    	text = bsUtils.PopupText("OO",color=(1, 1, 1), scale=0.75, randomOffset=0.2, offset=(0,-1,0), position=(node.position[0],node.position[1]-1.2,node.position[2])).autoRetain()
                    bs.gameTimer(1460,bs.Call(look))
                    bs.gameTimer(2960,bs.Call(look))
                    bs.gameTimer(5460,bs.Call(look))
                    bs.gameTimer(7960,bs.Call(look))        
                elif self.blastType == "curseBomb":
                    node.handleMessage(bs.PowerupMessage(powerupType='curse'))

        else:
            bs.Actor.handleMessage(self, msg)

    

class Bomb(bs.Actor):
    """
    category: Game Flow Classes
    
    A bomb and its variants such as land-mines and tnt-boxes.
    """

    def __init__(self, position=(0,1,0), velocity=(0,0,0), bombType='normal',
                 blastRadius=2.0, sourcePlayer=None, owner=None):
        """
        Create a new Bomb.
        
        bombType can be 'ice','impact','landMine','normal','sticky', or 'tnt'.
        Note that for impact or landMine bombs you have to call arm()
        before they will go off.
        """
        bs.Actor.__init__(self)
        self.aim = None
        factory = self.getFactory()

        if not bombType in ('ice','impact','landMine','normal','banana','sleepPotion','forceBomb','toxic','enderPearl','elonMine','sticky','tnt','weedbomb','shockWave','curseBomb'):
            raise Exception("invalid bomb type: " + bombType)
        self.bombType = bombType

        self._exploded = False

        if self.bombType == 'sticky' or self.bombType == 'forceBomb':
            self._lastStickySoundTime = 0

        self.blastRadius = blastRadius
        if self.bombType == 'ice': self.blastRadius *= 1.2
        elif self.bombType == 'impact': self.blastRadius *= 0.7
        elif self.bombType == 'landMine': self.blastRadius *= 0.7
        elif self.bombType == 'enderPearl': self.blastRadius *= 0.4
        elif self.bombType == 'toxic': self.blastRadius *= 1.2
        elif self.bombType == 'banana': self.blastRadius *= 0.6
        elif self.bombType == 'sleepPotion': self.blastRadius *= 1.2
        elif self.bombType == 'elonMine': self.blastRadius *= 1.0
        elif self.bombType == 'shockWave': self.blastRadius *= 0.2
        elif self.bombType == 'tnt': self.blastRadius *= 1.45

        self._explodeCallbacks = []
        
        # the player this came from
        self.sourcePlayer = sourcePlayer

        # by default our hit type/subtype is our own, but we pick up types of
        # whoever sets us off so we know what caused a chain reaction
        self.hitType = 'explosion'
        self.hitSubType = self.bombType

        # if no owner was provided, use an unconnected node ref
        if owner is None: owner = bs.Node(None)

        # the node this came from
        self.owner = owner

        def _addTrail(self):
              if self.node.exists():
                  bs.emitBGDynamics(position=self.node.position,velocity=(0,1,0),count=0,spread=0.05,scale=0,chunkType='spark')
              else: 
                  self._trailTimer = None
        def _addTrails(self):
              if self.node.exists():
                  bs.emitBGDynamics(position=self.node.position,velocity=(0,1,0),count=0,spread=0.5,scale=0,chunkType='spark')
              else: 
                  self._trailTimer = None

        # adding footing-materials to things can screw up jumping and flying
        # since players carrying those things
        # and thus touching footing objects will think they're on solid ground..
        # perhaps we don't wanna add this even in the tnt case?..
        if self.bombType == 'tnt':
            materials = (factory.bombMaterial,
                         bs.getSharedObject('footingMaterial'),
                         bs.getSharedObject('objectMaterial'))
        else:
            materials = (factory.bombMaterial,
                         bs.getSharedObject('objectMaterial'))
            
        if self.bombType in ['impact','sleepPotion','banana','enderPearl','weedbomb','shockWave','curseBomb']:
            materials = materials + (factory.impactBlastMaterial,)
        elif self.bombType in ['landMine','elonMine']:
            materials = materials + (factory.landMineNoExplodeMaterial,)

        if self.bombType in ['sticky','forceBomb']:
            materials = materials + (factory.stickyMaterial,)
        else:
            materials = materials + (factory.normalSoundMaterial,)

        if self.bombType == 'landMine':
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position':position,
                'velocity':velocity,
                'model':factory.landMineModel,
                'lightModel':factory.landMineModel,
                'body':'landMine',
                'shadowSize':0.44,
                'colorTexture':factory.landMineTex,
                'reflection':'powerup',
                'reflectionScale':[1.0],
                'materials':materials})
            self._trailTimer = bs.Timer(10,bs.Call(_addTrail,self),repeat=True)

        elif self.bombType == 'tnt':
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position':position,
                'velocity':velocity,
                'model':factory.tntModel,
                'lightModel':factory.tntModel,
                'body':'crate',
                'shadowSize':0.5,
                'colorTexture':factory.tntTex,
                'reflection':'soft',
                'reflectionScale':[0.23],
                'materials':materials})
            self._trailTimer = bs.Timer(1,bs.Call(_addTrails,self),repeat=True)
            
        elif self.bombType == 'shockWave':
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position': position,
                'velocity': velocity,
                'model': factory.shockWaveModel,
                'body': 'capsule',
                'bodyScale': 0.4,
                'shadowSize': 0.5,
                'bodyScale': 0.9,
                'modelScale': 1.3,
                'colorTexture': factory.shockWaveTex,
                'reflection': 'soft',
                'reflectionScale': [0.7],
                'materials': materials})
            self._trailTimer = bs.Timer(10,bs.Call(_addTrail,self),repeat=True)            

        elif self.bombType == 'weedbomb':
            fuseTime = 20000
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position': position,
                'velocity': velocity,
                'body': 'sphere',
                'model': factory.weedbombModel,
                'shadowSize': 0.3,
                'colorTexture': factory.weedbombTex,
                'reflection': 'powerup',
                'reflectionScale': [1.5],
                'materials': materials})           

        elif self.bombType == 'curseBomb':
            fuseTime = 20000
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position': position,
                'velocity': velocity,
                'body': 'sphere',
                'model': factory.curseBombModel,
                'shadowSize': 0.3,
                'colorTexture': factory.curseBombTex,
                'reflection': 'soft',
                'reflectionScale': [0.5],
                'materials': materials})
                
        elif self.bombType == 'forceBomb':
            self.node = bs.newNode('prop', delegate=self, owner=owner, attrs={
                'position': position,
                'velocity': velocity,
                'model': factory.stickyBombModel,
                'lightModel': factory.stickyBombModel,
                'body': 'sphere',
                
                'shadowSize': 0.44,
                'colorTexture': factory.forceTex,
                'reflection': 'powerup',
                'reflectionScale': [1.0],
                'materials': materials})
            self._trailTimer = bs.Timer(10,bs.Call(_addTrail,self),repeat=True)
            self._light = bs.newNode('light',attrs={'position':position,'radius':0.3,
                                     'color': (0.20,0.53,1), 'volumeIntensityScale':1.0})
            bsUtils.animate(self._light,"intensity",{0:0,100:1})
            self.node.connectAttr('position',self._light,'position')
        elif self.bombType == 'banana':
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position': position,
                'velocity': velocity,
                'model': factory.bananaModel,
                'body': 'capsule',
                'bodyScale': 0.4,
                'shadowSize': 0.5,
                'bodyScale': 0.8,
                'density': 1,
                'colorTexture': factory.bananaTex,
                'reflection': 'soft',
                'reflectionScale': [0.4],
                'materials': materials})
            self._trailTimer = bs.Timer(10,bs.Call(_addTrail,self),repeat=True)
                       
        elif self.bombType == 'sleepPotion':
            self.node = bs.newNode('prop',
                                   delegate=self,
                                   attrs={'position':position,
                                          'velocity':velocity,
                                          'body':'sphere',
                                          'shadowSize':0.0,
                                          'reflection':'powerup',
                                          'reflectionScale':[1.1],
                                          'materials':materials})
            self._trailTimer = bs.Timer(10,bs.Call(_addTrail,self),repeat=True)
            self.shield1 = bs.newNode('shield',owner=self.node,
                                     attrs={'color':(1,1,1),'radius':0.6})
            self.node.connectAttr('position',self.shield1,'position')
            
            self.shield2 = bs.newNode('shield',owner=self.node,
                                     attrs={'color':(20,0,20),'radius':0.4})
            self.node.connectAttr('position',self.shield2,'position')
            
            bs.animate(self.shield2,'radius',{0:0.1,300:0.5,600:0.1},True)            
            self._light = bs.newNode('light',attrs={'position':position,'radius':0.3,
                                     'color': (1,0,1), 'volumeIntensityScale':1.0})
            bsUtils.animate(self._light,"intensity",{0:0,100:1})
            self.node.connectAttr('position',self._light,'position')

        elif self.bombType == 'enderPearl':
            self.node = bs.newNode('prop',
                                   delegate=self,
                                   attrs={'position':position,
                                          'velocity':velocity,
                                          'body':'sphere',
                                          'bodyScale':0.85,
                                          'shadowSize':0.5,
                                          'materials':materials})
            self._trailTimer = bs.Timer(10,bs.Call(_addTrail,self),repeat=True)
                                          
            self.shield1 = bs.newNode('shield',owner=self.node,
                                     attrs={'color':(1,1,1),'radius':0.6})
            self.node.connectAttr('position',self.shield1,'position')
            
            self.shield2 = bs.newNode('shield',owner=self.node,
                                     attrs={'color':(20,0,0),'radius':0.4})
            self.node.connectAttr('position',self.shield2,'position')
            
            bs.animate(self.shield2,'radius',{0:0.1,300:0.5,600:0.1},True)

        elif self.bombType == 'elonMine':
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position': position,
                'velocity': velocity,
                'model': factory.elonMineModel,
                'lightModel': factory.elonMineModel,
                'body': 'landMine',
                'shadowSize': 0.44,
                'colorTexture': factory.elonMineTex,
                'reflection': 'powerup',
                'reflectionScale': [1.0],
                'materials': materials})
            self._trailTimer = bs.Timer(10,bs.Call(_addTrail,self),repeat=True)
            
        elif self.bombType == 'impact':
            fuseTime = 20000
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position':position,
                'velocity':velocity,
                'body':'sphere',
                'model':factory.impactBombModel,
                'shadowSize':0.3,
                'colorTexture':factory.impactTex,
                'reflection':'powerup',
                'reflectionScale':[1.5],
                'materials':materials})
            self._trailTimer = bs.Timer(10,bs.Call(_addTrail,self),repeat=True)
            self.armTimer = bs.Timer(200, bs.WeakCall(self.handleMessage,
                                                      ArmMessage()))
            self.warnTimer = bs.Timer(fuseTime-1700,
                                      bs.WeakCall(self.handleMessage,
                                                  WarnMessage()))

        else:
            fuseTime = 3000
            if self.bombType == 'sticky':
                sticky = True
                model = factory.stickyBombModel
                rType = 'sharper'
                rScale = 1.8
            elif self.bombType == 'forceBomb':
                sticky = True
                model = factory.stickyBombModel
                rType = 'sharper'
                rScale = 1.8
            elif self.bombType == 'toxic':
                sticky = True
                model = factory.bombModel
                rType = 'sharper'
                rScale = 0.0
            else:
                sticky = False
                model = factory.bombModel
                rType = 'sharper'
                rScale = 1.8
            if self.bombType == 'ice': tex = factory.iceTex
            elif self.bombType == 'toxic': tex = factory.radioactiveTex
            elif self.bombType == 'sticky': tex = factory.stickyTex
            else: tex = factory.regularTex
            
            self.node = bs.newNode('bomb', delegate=self, attrs={
                'position': position,
                'velocity': velocity,
                'model': model,
                #'bodyScale': 0.6,
                'shadowSize': 0.3,
                'colorTexture': tex,
                'sticky': sticky,
                'owner': owner,
                'reflection': rType,
                'reflectionScale':[rScale] if bombType != 'normal' else ((0+random.random()*20.0),(0+random.random()*20.0),(0+random.random()*20.0)),
                'materials': materials})

            sound = bs.newNode('sound', owner=self.node, attrs={
                'sound':factory.fuseSound,
                'volume':0.25})
            self.node.connectAttr('position', sound, 'position')
            bsUtils.animate(self.node, 'fuseLength', {0:1.0, fuseTime:0.0})

        # light the fuse!!!
        if self.bombType not in ('landMine','elonMine','sleepPotion','banana','forceBomb','enderPearl','tnt','shockWave'):
            bs.gameTimer(fuseTime, bs.WeakCall(self.handleMessage, ExplodeMessage()))
            animate = True
            prefixAnim = {0: (1, 0, 0), 250: (1, 1, 0), 250 * 2: (0, 1, 0), 250 * 3: (0, 1, 1), 250 * 4: (1, 0, 1),
                          250 * 5: (0, 0, 1), 250 * 6: (1, 0, 0)}
            if hack.shieldBomb:               
                self.shield = bs.newNode('shield', owner=self.node,
                attrs={'color':(0,0,1),'radius':0.6})
                self.node.connectAttr('position', self.shield, 'position')   
                bs.animate(self.shield,'radius',{0:0.9,200:1,400:0.9},True)
                bsUtils.animateArray(self.shield, 'color', 3, prefixAnim, True)        
            if hack.bombLights:
                self.nodeLight = bs.newNode('light',
                attrs={'position': self.node.position,
                'color': (0,0,1),'radius': 0.1,'volumeIntensityScale': 0.2})
                self.node.connectAttr('position', self.nodeLight, 'position')
                bs.gameTimer(1000,self.nodeLight.delete)  
                bs.animateArray(self.nodeLight,'color',3,{0:(0,0,2),500:(0,2,0),1000:(2,0,0),1500:(2,2,0),2000:(2,0,2),2500:(0,1,6),3000:(1,2,0)},True) 
                bs.animate(self.nodeLight, "intensity", {0:1.0, 1000:1.8, 2000:1.0}, loop = True)                  
            if hack.bombName:
                m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 0.5, 0), 'operation': 'add'})
                self.node.connectAttr('position', m, 'input2')
                self.nodeText = bs.newNode('text',
                                           owner=self.node,
                                           attrs={'text': bombType,
                                                  'inWorld': True,
                                                  'shadow': 1.0,
                                                  'flatness': 1.0,
                                                  'color': (1,1,1),
                                                  'scale': 0.0,
                                                  'hAlign': 'center'})
                m.connectAttr('output', self.nodeText, 'position')
                bs.animate(self.nodeText, 'scale', {0: 0, 140: 0.0125, 200: 0.01})
                if hack.animate:
                    bs.animateArray(self.nodeText,'color',3,{0:(2,2,0),600:(2,0,0),900:(0,2,0),1200:(0,0,2),1500:(2,0,2), 1800:(2,1,0),2100:(0,2,2),2400:(2,2,0)},True)
                    bs.emitBGDynamics(position=self.nodeText.position, velocity=self.node.position, count=200, scale=1.4, spread=2.01, chunkType='spark')
                    
        if self.bombType == 'toxic': bsUtils.animate(self.node,"modelScale",{0:0, 200:1.3, 260:1.0, 2800:1.0, 2900:0.6, 3000:2.0})
    	else: bsUtils.animate(self.node,"modelScale",{0:0, 200:1.3, 260:1})
            
                                  
    def getSourcePlayer(self):
        """
        Returns a bs.Player representing the source of this bomb.
        """
        if self.sourcePlayer is None: return bs.Player(None) # empty player ref
        return self.sourcePlayer
        
    @classmethod
    def getFactory(cls):
        """
        Returns a shared bs.BombFactory object, creating it if necessary.
        """
        activity = bs.getActivity()
        try: return activity._sharedBombFactory
        except Exception:
            f = activity._sharedBombFactory = BombFactory()
            return f

    def onFinalize(self):
        bs.Actor.onFinalize(self)
        # release callbacks/refs so we don't wind up with dependency loops..
        self._explodeCallbacks = []
        
    def _handleDie(self,m):
        self.node.delete()
        
    def _handleOOB(self, msg):
        self.handleMessage(bs.DieMessage())

    def _handleImpact(self,m):
        node,body = bs.getCollisionInfo("opposingNode","opposingBody")
        # if we're an impact bomb and we came from this node, don't explode...
        # alternately if we're hitting another impact-bomb from the same source,
        # don't explode...
        try: nodeDelegate = node.getDelegate()
        except Exception: nodeDelegate = None
        if node is not None and node.exists():
            if (self.bombType in ['impact','elonMine','banana','shockWave'] and
                (node is self.owner
                 or (isinstance(nodeDelegate, Bomb)
                     and nodeDelegate.bombType == 'impact'
                     and nodeDelegate.owner is self.owner))): return
            elif (self.bombType == 'enderPearl' and (node is self.owner or (isinstance(nodeDelegate,Bomb) and nodeDelegate.bombType == 'enderPearl' and nodeDelegate.owner is self.owner))): return
            elif (self.bombType == 'sleepPotion' and (node is self.owner or (isinstance(nodeDelegate,Bomb) and nodeDelegate.bombType == 'sleepPotion' and nodeDelegate.owner is self.owner))): return
            elif (self.bombType == 'weedbomb' and (node is self.owner or (isinstance(nodeDelegate,Bomb) and nodeDelegate.bombType == 'weedbomb' and nodeDelegate.owner is self.owner))): return
            elif (self.bombType == 'curseBomb' and (node is self.owner or (isinstance(nodeDelegate,Bomb) and nodeDelegate.bombType == 'curseBomb' and nodeDelegate.owner is self.owner))): return
            else:
                self.handleMessage(ExplodeMessage())

    def _handleForceBomb(self, m, node):
        if self.node.exists():
            if node is not None and node is not self.owner \
                    and bs.getSharedObject('playerMaterial') in node.materials:
                self.node.sticky = True
                def on():
                    if self.node is not None and self.node.exists():
                        self.node.extraAcceleration = (0, 80, 0)

                    if self.aim is not None:
                        self.aim.off()

                bs.gameTimer(1, on)

    def _handleDropped(self,m):
        if self.bombType == 'landMine':
            self.armTimer = \
                bs.Timer(1250, bs.WeakCall(self.handleMessage, ArmMessage()))
        elif self.bombType == 'elonMine':
            self.armTimer = \
                bs.Timer(500, bs.WeakCall(self.handleMessage, ArmMessage()))
        elif self.bombType == 'forceBomb':
            self.armTimer = \
                bs.Timer(250, bs.WeakCall(self.handleMessage, ArmMessage()))

        # once we've thrown a sticky bomb we can stick to it..
        elif self.bombType == 'sticky':
            def _safeSetAttr(node,attr,value):
                if node.exists(): setattr(node,attr,value)
            bs.gameTimer(
                250, lambda: _safeSetAttr(self.node, 'stickToOwner', True))

    def _handleSplat(self,m):
        node = bs.getCollisionInfo("opposingNode")
        if (node is not self.owner
                and bs.getGameTime() - self._lastStickySoundTime > 1000):
            self._lastStickySoundTime = bs.getGameTime()
            bs.playSound(self.getFactory().stickyImpactSound, 2.0,
                         position=self.node.position)

    def addExplodeCallback(self,call):
        """
        Add a call to be run when the bomb has exploded.
        The bomb and the new blast object are passed as arguments.
        """
        self._explodeCallbacks.append(call)
        
    def explode(self):
        """
        Blows up the bomb if it has not yet done so.
        """
        if self._exploded: return
        self._exploded = True
        activity = self.getActivity()
        if activity is not None and self.node.exists():
            blast = Blast(
                position=self.node.position,
                velocity=self.node.velocity,
                blastRadius=self.blastRadius,
                blastType=self.bombType,
                sourcePlayer=self.sourcePlayer,
                hitType=self.hitType,
                hitSubType=self.hitSubType).autoRetain()
            for c in self._explodeCallbacks: c(self,blast)
        if self.bombType == 'enderPearl':
                pos = self.node.position
                self.owner.handleMessage(bs.StandMessage((pos[0],pos[1]-0.9,pos[2])))
                blast = Blast(position=self.node.position,velocity=self.node.velocity,blastRadius=0,blastType=self.bombType,sourcePlayer=self.sourcePlayer,hitType=self.hitType,hitSubType=self.hitSubType).autoRetain()   
        elif self.bombType == 'sleepPotion':
                blast = Blast(position=self.node.position,velocity=self.node.velocity,blastRadius=self.blastRadius,blastType=self.bombType,sourcePlayer=self.sourcePlayer,hitType=self.hitType,hitSubType=self.hitSubType).autoRetain()
                self._light.delete()
        elif self.bombType == 'shockWave':
            	bdUtils.ShockWave(position=self.node.position)
            	bs.playSound(self.getFactory().shockWaveSound, position=self.node.position)                
        # we blew up so we need to go away
        bs.gameTimer(1, bs.WeakCall(self.handleMessage, bs.DieMessage()))

    def _handleWarn(self, m):
        if self.textureSequence.exists():
            self.textureSequence.rate = 30
            bs.playSound(self.getFactory().warnSound, 0.5,
                         position=self.node.position)

    def _addMaterial(self, material):
        if not self.node.exists(): return
        materials = self.node.materials
        if not material in materials:
            self.node.materials = materials + (material,)
        
    def arm(self):
        """
        Arms land-mines and impact-bombs so
        that they will explode on impact.
        """
        if not self.node.exists(): return
        factory = self.getFactory()
        if self.bombType == 'landMine':
            self.textureSequence = \
                bs.newNode('textureSequence', owner=self.node, attrs={
                    'rate':30,
                    'inputTextures':(factory.landMineLitTex,
                                     factory.landMineTex)})
            bs.gameTimer(500,self.textureSequence.delete)
            # we now make it explodable.
            bs.gameTimer(250,bs.WeakCall(self._addMaterial,
                                         factory.landMineBlastMaterial))
        elif self.bombType == 'elonMine':
            self.textureSequence = \
                bs.newNode('textureSequence', owner=self.node, attrs={
                    'rate': 30,
                    'inputTextures': (factory.elonMineLitTex,
                                      factory.elonMineTex)})

            bs.gameTimer(500, self.textureSequence.delete)
            bs.playSound(bs.getSound('activateBeep'), position=self.node.position)
            self.aim = bdUtils.AutoAim(self.node, self.owner)
            # we now make it explodable.
            bs.gameTimer(250, bs.WeakCall(self._addMaterial,
                                          factory.landMineBlastMaterial))
        elif self.bombType == 'forceBomb':
            bs.playSound(bs.getSound('activateBeep'), position=self.node.position)
            self.aim = bdUtils.AutoAim(self.node, self.owner)
        elif self.bombType == 'impact':
            self.textureSequence = \
                bs.newNode('textureSequence', owner=self.node, attrs={
                    'rate':100,
                    'inputTextures':(factory.impactLitTex,
                                     factory.impactTex,
                                     factory.impactTex)})
            bs.gameTimer(250, bs.WeakCall(self._addMaterial,
                                          factory.landMineBlastMaterial))
        else:
            raise Exception('arm() should only be called '
                            'on land-mines or impact bombs')
        if not self.bombType == 'forceBomb':
            self.textureSequence.connectAttr('outputTexture',
                                             self.node, 'colorTexture')

            bs.playSound(factory.activateSound, 0.5, position=self.node.position)
        
    def _handleHit(self, msg):
        isPunch = (msg.srcNode.exists() and msg.srcNode.getNodeType() == 'spaz')

        # normal bombs are triggered by non-punch impacts..
        # impact-bombs by all impacts
        if (not self._exploded and not isPunch
            or self.bombType in ['impact', 'landMine', 'elonMine','weedbomb','curseBomb']):
            # also lets change the owner of the bomb to whoever is setting
            # us off.. (this way points for big chain reactions go to the
            # person causing them)
            if msg.sourcePlayer not in [None]:
                self.sourcePlayer = msg.sourcePlayer

                # also inherit the hit type (if a landmine sets off by a bomb,
                # the credit should go to the mine)
                # the exception is TNT.  TNT always gets credit.
                if self.bombType != 'tnt':
                    self.hitType = msg.hitType
                    self.hitSubType = msg.hitSubType

            bs.gameTimer(100+int(random.random()*100),
                         bs.WeakCall(self.handleMessage, ExplodeMessage()))
        self.node.handleMessage(
            "impulse", msg.pos[0], msg.pos[1], msg.pos[2],
            msg.velocity[0], msg.velocity[1], msg.velocity[2],
            msg.magnitude, msg.velocityMagnitude, msg.radius, 0,
            msg.velocity[0], msg.velocity[1], msg.velocity[2])

        if msg.srcNode.exists():
            pass
        
    def handleMessage(self, msg):
        if isinstance(msg, ExplodeMessage): self.explode()
        elif isinstance(msg, SetStickyMessage):
            node = bs.getCollisionInfo('opposingNode')
            self._handleForceBomb(msg, node)
        elif isinstance(msg, ImpactMessage): self._handleImpact(msg)
        elif isinstance(msg, bs.PickedUpMessage):
            if self.bombType == 'elonMine' \
                    and self.node.exists() \
                    and self.owner != msg.node:
                bs.playSound(
                    bs.getSound('corkPop'),
                    position=self.node.position)

                bsUtils.PopupText(
                    bs.Lstr(resource='elonMineDefused'),
                    color=(1, 1, 1),
                    scale=1.0,
                    position=self.node.position).autoRetain()

                self.node.delete()
            
            # change our source to whoever just picked us up *only* if its None
            # this way we can get points for killing bots with their own bombs
            # hmm would there be a downside to this?...
            if self.sourcePlayer is not None:
                self.sourcePlayer = msg.node.sourcePlayer
        elif isinstance(msg, SplatMessage): self._handleSplat(msg)
        elif isinstance(msg, bs.DroppedMessage): self._handleDropped(msg)
        elif isinstance(msg, bs.HitMessage): self._handleHit(msg)
        elif isinstance(msg, bs.DieMessage): self._handleDie(msg)
        elif isinstance(msg, bs.OutOfBoundsMessage): self._handleOOB(msg)
        elif isinstance(msg,ToxicMessage): self.explode()
        elif isinstance(msg, ArmMessage): self.arm()
        elif isinstance(msg,SleepMessage): self.explode()
        elif isinstance(msg, WarnMessage): self._handleWarn(msg)
        else: bs.Actor.handleMessage(self, msg)

class TNTSpawner(object):
    """
    category: Game Flow Classes

    Regenerates TNT at a given point in space every now and then.
    """
    def __init__(self,position,respawnTime=30000):
        """
        Instantiate with a given position and respawnTime (in milliseconds).
        """
        self._position = position
        self._tnt = None
        self._update()
        self._updateTimer = bs.Timer(1000,bs.WeakCall(self._update),repeat=True)
        self._respawnTime = int(random.uniform(0.8,1.2)*respawnTime)
        self._waitTime = 0
        
    def _update(self):
        tntAlive = self._tnt is not None and self._tnt.node.exists()
        if not tntAlive:
            # respawn if its been long enough.. otherwise just increment our
            # how-long-since-we-died value
            if self._tnt is None or self._waitTime >= self._respawnTime:
                self._tnt = Bomb(position=self._position,bombType='tnt')
                self._waitTime = 0
            else: self._waitTime += 1000
