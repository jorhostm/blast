!$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
!$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
!     Subroutine vuhard
!$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
!$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
      subroutine vuhard(
     . nblock,
     . jElem, kIntPt, kLayer, kSecPt,
     . lAnneal, stepTime, totalTime, dt, cmname,
     . nstatev, nfieldv, nprops,
     . props, tempOld, tempNew, fieldOld, fieldNew,
     . stateOld,
     . eqps, eqpsRate,
     . yield, dyieldDtemp, dyieldDeqps,
     . stateNew)
      include 'vaba_param.inc'
!-----Data from ABAQUS
      dimension props(nprops), tempOld(nblock), tempNew(nblock),
     . fieldOld(nblock,nfieldv), fieldNew(nblock,nfieldv),
     . stateOld(nblock,nstatev), eqps(nblock), eqpsRate(nblock),
     . yield(nblock), dyieldDtemp(nblock), dyieldDeqps(nblock,2),
     . stateNew(nblock,nstatev), jElem(nblock)
      character*80 cmname
!-----material parameters
      real*8 sigma0,THETAR1,QR1,THETAR2,QR2,THETAR3,QR3
!-----Internal variables
      integer i
      real*8 THETAR1oQR1,THETAR2oQR2,THETAR3oQR3
      integer iflVUHARD
      data iflVUHARD/0/
!-----------------------------------------------------------------------
!     Read material properties
!-----------------------------------------------------------------------
      sigma0  = props(1)
      THETAR1 = props(2)
      QR1     = props(3)
      THETAR2 = props(4)
      QR2     = props(5)
      THETAR3 = props(6)
      QR3     = props(7)
!-----------------------------------------------------------------------
!     Prepare material properties
!-----------------------------------------------------------------------
      if(QR1.gt.0.0)then
         THETAR1oQR1 = THETAR1/QR1
      else
         THETAR1oQR1 = 0.0
      endif
      if(QR2.gt.0.0)then
         THETAR2oQR2 = THETAR2/QR2
      else
         THETAR2oQR2 = 0.0
      endif
      if(QR3.gt.0.0)then
         THETAR3oQR3 = THETAR3/QR3
      else
         THETAR3oQR3 = 0.0
      endif
!-----------------------------------------------------------------------
!     Print parameters when time = 0.0
!-----------------------------------------------------------------------
      if(iflVUHARD.eq.0)then
         write(6,'(a30)') '______________________________'
         write(6,'(a30)') '|                            |'
         write(6,'(a30)') '|  SIMLab Metal Model        |'
         write(6,'(a30)') '|  VUHARD                    |'
         write(6,'(a30)') '|____________________________|'
         write(6,*)
         write(6,'(a10,es14.6)') 'sigma0   =', sigma0
         write(6,'(a10,es14.6)') 'THETAR1  =', THETAR1
         write(6,'(a10,es14.6)') 'QR1      =', QR1
         write(6,'(a10,es14.6)') 'THETAR2  =', THETAR2
         write(6,'(a10,es14.6)') 'QR2      =', QR2
         write(6,'(a10,es14.6)') 'THETAR3  =', THETAR3
         write(6,'(a10,es14.6)') 'QR3      =', QR3
         iflVUHARD = 1
      endif
!-----------------------------------------------------------------------
!     Compute yield stress and derivatives
!-----------------------------------------------------------------------
      do i=1,nblock
         yield(i)         = sigma0+QR1*(1.0-exp(-THETAR1oQR1*eqps(i)))
     +                            +QR2*(1.0-exp(-THETAR2oQR2*eqps(i)))
     +                            +QR3*(1.0-exp(-THETAR3oQR3*eqps(i)))
         dyieldDeqps(i,1) = THETAR1*exp(-THETAR1oQR1*eqps(i))
     +                     +THETAR2*exp(-THETAR2oQR2*eqps(i))
     +                     +THETAR3*exp(-THETAR3oQR3*eqps(i))
         dyieldDeqps(i,2) = 0.0
         dyieldDtemp(i)   = 0.0
      enddo
!-----------------------------------------------------------------------
!     Compute yield stress and derivatives
!-----------------------------------------------------------------------
      do i=1,nblock
         statenew(i,1) = eqps(i)
      enddo
!-----------------------------------------------------------------------
!     End of subroutine
!-----------------------------------------------------------------------
      return
      end