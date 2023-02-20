      include 'VDLOAD.f'
      include 'VUHARD.f'
!$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
!$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
!     Subroutine vusdfld
!$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
!$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
      subroutine vusdfld(
     . nblock, nstatev, nfieldv, nprops, ndir, nshr,
     . jElem, kIntPt, kLayer, kSecPt,
     . stepTime, totalTime, dt, cmname,
     . coordMp, direct, Tabaq, charLength, props,
     . stateOld,
     . stateNew,field)
      include 'vaba_param.inc'
#include <SMAAspUserSubroutines.hdr>
!      include 'SMAAspUserUtilities.hdr'
!      include 'SMAAspUserArrays.hdr'
!-----Data from ABAQUS
      dimension jElem(nblock),coordMp(nblock,*),direct(nblock,3,3),
     .          Tabaq(nblock,3,3),charLength(nblock),props(nprops),
     .          stateOld(nblock,nstatev),stateNew(nblock,nstatev),
     .          field(nblock,nfieldv)
      character*80 cmname,CPNAME
!-----Data from ABAQUS
      dimension stressdata(maxblk*(ndir+nshr))
      dimension pedata(maxblk*(ndir+nshr))
      dimension ledata(maxblk*(ndir+nshr))
      dimension peeqdata(maxblk),dummy(maxblk),thdata(maxblk)
      dimension eigVal(nblock,3),s(nblock,6)
      integer jSData(maxblk*(ndir+nshr)),jPData(maxblk)
      character*3 cPData(maxblk),cSData(maxblk*(ndir+nshr))
      integer jStatus
c
      integer kNel,kInc,kSecPt
!-----material parameters
      real*8 DCRIT,WcB,WcS,WcL,c,phi,gamma,te
!-----Internal variables
      integer i
      real*8 dp(nblock)
      real*8 sigp1(nblock),sigp3(nblock),seq(nblock)
      real*8 pe(nblock,3),le(nblock,3),leote(nblock)
      real*8 damage(nblock),WcM,omega(nblock),Wc(nblock)
      integer iflVUSDFLD
      data iflVUSDFLD/0/
!-----Plastic thinning
      real*8 eps3(1)
      pointer(ptrE,eps3)
!-----Failure status
      real*8 status(1)
      pointer(ptrS,status)
!-----Failure status
      real*8 fail(1)
      pointer(ptrF,fail)
!-----Bending indicator
      real*8 failureweight(1)
      pointer(ptrW,failureweight)
!-----Integer parameters
      integer INTCM(20)
      pointer(ptrC,INTCM)
      integer jElement(nblock)
!-----------------------------------------------------------------------
!     Read material properties
!-----------------------------------------------------------------------
      DCRIT = props(1)
      WcB   = props(2)
      WcS   = props(3)
      WcL   = props(4)
      c     = props(5)
      phi   = props(6)
      gamma = props(7)
      te    = props(8)
!-----------------------------------------------------------------------
!     Print material properties at time = 0.0
!-----------------------------------------------------------------------
      if(iflVUSDFLD.eq.0)then
         write(6,'(a30)') '______________________________'
         write(6,'(a30)') '|                            |'
         write(6,'(a30)') '|  SIMLab Metal Model        |'
         write(6,'(a30)') '|  VUSDFLD                   |'
         write(6,'(a30)') '|____________________________|'
         write(6,*)
         write(6,'(a10,es14.6)') 'DCRIT    =',DCRIT
         write(6,'(a10,es14.6)') 'WcB      =',WcB
         write(6,'(a10,es14.6)') 'WcL      =',WcL
         write(6,'(a10,es14.6)') 'WcS      =',WcS
         write(6,'(a10,es14.6)') 'c        =',c
         write(6,'(a10,es14.6)') 'phi      =',phi
         write(6,'(a10,es14.6)') 'gamma    =',gamma
         write(6,'(a10,es14.6)') 'te       =',te
         iflVUSDFLD = 1
      endif
!-----------------------------------------------------------------------
!     Call history variables
!-----------------------------------------------------------------------
      call vgetvrm(  'S' , stressdata,jSData,cSData,jStatus)
      call vgetvrm('PEEQ',   peeqdata,jPData,cPData,jStatus)
      call vgetvrm(  'PE',     pedata,jSData,cSData,jStatus)
      call vgetvrm(  'LE',     ledata,jSData,cSData,jStatus)
      call vgetvrm( 'STH',     thdata,jSData,cSData,jStatus)
!-----------------------------------------------------------------------
!        Access parameters in memory
!-----------------------------------------------------------------------
      ptrC = SMAIntArrayAccess(3)
!-----------------------------------------------------------------------
!        Read parameters in memory
!-----------------------------------------------------------------------
      kNel = INTCM(1)
      kInc = INTCM(2)
!-----------------------------------------------------------------------
!        Set up number of integration points through the thickness
!-----------------------------------------------------------------------
      if(kInc.eq.1)then
         INTCM(3) = max(INTCM(3),kSecPt)
      endif
!-----------------------------------------------------------------------
!     Grab element aspect ratio
!-----------------------------------------------------------------------
      if(kInc.eq.1)then
         do i=1,nblock
            leote(i) = charLength(i)/te
            omega(i) = 0.0
         enddo
      endif
c
      if(kInc.gt.1)then
         ptrW = SMAFloatArrayAccess(2)
         do i=1,nblock
            omega(i) = failureweight(jElem(i))
            leote(i) = stateOld(i,3)
         enddo
      endif
!-----------------------------------------------------------------------
!     Extract data
!-----------------------------------------------------------------------
      do i=1,nblock
         dp(i)     = peeqdata(i)-stateOld(i,1)
         damage(i) = stateOld(i,2)
      enddo
!-----------------------------------------------------------------------
!     Compute equivalent stress (von Mises)
!-----------------------------------------------------------------------
      if(nshr.gt.1)then
         do i=1,nblock
            s(i,1) = stressdata(i)
            s(i,2) = stressdata(i+nblock)
            s(i,3) = stressdata(i+nblock*2)
            s(i,4) = stressdata(i+nblock*3)
            s(i,5) = stressdata(i+nblock*4)
            s(i,6) = stressdata(i+nblock*5)
            seq(i) = sqrt(s(i,1)*s(i,1)+s(i,2)*s(i,2)
     +                   +s(i,3)*s(i,3)
     +                   -s(i,1)*s(i,2)-s(i,2)*s(i,3)
     +                   -s(i,3)*s(i,1)
     +                   +3.0*(s(i,4)*s(i,4)+s(i,5)*s(i,5)
     +                   +s(i,6)*s(i,6)))
         enddo
!-----------------------------------------------------------------------
!        Compute Wc parameter for solids
!-----------------------------------------------------------------------
         do i=1,nblock
            Wc(i) = WcB
         enddo
      else
         do i=1,nblock
            s(i,1) = stressdata(i)
            s(i,2) = stressdata(i+nblock)
            s(i,3) = stressdata(i+nblock*2)
            s(i,4) = stressdata(i+nblock*3)
            seq(i) = sqrt(s(i,1)*s(i,1)+s(i,2)*s(i,2)
     +                   -s(i,1)*s(i,2)+3.0*s(i,4)*s(i,4))
c
            pe(i,1)  = pedata(i)
            pe(i,2)  = pedata(i+nblock)
            pe(i,3)  = pedata(i+nblock*2)
         enddo
!-----------------------------------------------------------------------
!        Compute Wc parameter for shells
!-----------------------------------------------------------------------
         do i=1,nblock
            WcM   = WcL+(WcS-WcL)*exp(-c*(leote(i)-1.0))
            Wc(i) = WcB*omega(i)+WcM*(1.0-omega(i))
         enddo
      endif
!-----------------------------------------------------------------------
!     Compute principal stresses
!-----------------------------------------------------------------------
      call vsprinc(nblock,s,eigVal,ndir,nshr)
      do i=1,nblock
         sigp1(i) = max(eigVal(i,1),eigVal(i,2),eigVal(i,3))
         sigp3(i) = min(eigVal(i,1),eigVal(i,2),eigVal(i,3))
      enddo
!-----------------------------------------------------------------------
!     Compute Extended Cockcroft-Latham damage
!-----------------------------------------------------------------------
      do i=1,nblock
         if(seq(i).gt.0.0)then
            damage(i) = damage(i)
     +     +dp(i)*seq(i)*max(0.0,((phi*sigp1(i)
     +     +(1.0-phi)*(sigp1(i)-sigp3(i)))/seq(i))**gamma)/Wc(i)
         endif
      enddo
!-----------------------------------------------------------------------
!     Check for fracture
!-----------------------------------------------------------------------
      do i=1,nblock
         if(damage(i).gt.DCRIT)then
            statenew(i,NSTATEV) = 0
         else
            statenew(i,NSTATEV) = 1
         endif
      enddo
!-----------------------------------------------------------------------
!     Update History Variables
!-----------------------------------------------------------------------
      do i=1,nblock
         stateNew(i,1) = peeqdata(i)
         statenew(i,2) = damage(i)
         statenew(i,3) = leote(i)
         statenew(i,4) = omega(i)
         statenew(i,5) = direct(i,3,3)
      enddo
!-----------------------------------------------------------------------
!     Update Damage in memory
!-----------------------------------------------------------------------
      if(kInc.gt.1)then
         ptrE = SMAFloatArrayAccess(5)
         ptrS = SMAFloatArrayAccess(6)
         ptrF = SMAFloatArrayAccess(7)
c
         do i=1,nblock
            k = jElem(i)+kNel*(kSecPt-1)
            eps3(k) = pe(i,3)
            status(k) = statenew(i,NSTATEV)
c
            if(fail(jElem(i)).gt.0.5)then
               statenew(i,NSTATEV) = 0
            endif
         enddo
      endif
!-----------------------------------------------------------------------
!     End of subroutine
!-----------------------------------------------------------------------
      return
      end
!$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
!$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
!     Subroutine vexternaldb
!$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
!$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
      subroutine vexternaldb(lOp, i_Array, niArray, r_Array, nrArray)
      include 'vaba_param.inc'
#include <SMAAspUserSubroutines.hdr>
!     Contents of i_Array
      parameter( i_int_nTotalNodes     = 1,
     *           i_int_nTotalElements  = 2,
     *           i_int_kStep           = 3,
     *           i_int_kInc            = 4,
     *           i_int_iStatus         = 5,
     *           i_int_lWriteRestart   = 6  )
!     Possible values for the lOp argument
      parameter( j_int_StartAnalysis    = 0,
     *           j_int_StartStep        = 1,
     *           j_int_SetupIncrement   = 2,
     *           j_int_StartIncrement   = 3,
     *           j_int_EndIncrement     = 4,
     *           j_int_EndStep          = 5,
     *           j_int_EndAnalysis      = 6 )
!     Possible values for i_Array(i_int_iStatus)
      parameter( j_int_Continue          = 0,
     *           j_int_TerminateStep     = 1,
     *           j_int_TerminateAnalysis = 2)
!     Contents of r_Array
      parameter( i_flt_TotalTime   = 1,
     *           i_flt_StepTime    = 2,
     *           i_flt_dTime       = 3 )
!
      dimension i_Array(niArray),r_Array(nrArray)
!-----------------------------------------------------------------------
!     Declaration of variables
!-----------------------------------------------------------------------
!-----Integration points locations
      real*8 eps3(1)
      pointer(ptrE,eps3)
c
      real*8 status(1)
      pointer(ptrS,status)
c
      real*8 fail(1)
      pointer(ptrF,fail)
c
      real*8 failureweight(1)
      pointer(ptrW,failureweight)
c
      real*8 maxeps3,mineps3
      real*8 eps3dw,eps3up,max2
!-----Integer parameters
      integer INTCM(20)
      pointer(ptrC,INTCM)
c
      integer i
      real*8 max_1
!-----------------------------------------------------------------------
!     Initialization
!-----------------------------------------------------------------------
      kStep = i_Array(i_int_kStep)
      kInc  = i_Array(i_int_kInc)
      kNel  = i_Array(i_int_nTotalElements)
!-----------------------------------------------------------------------
!     Start of the analysis
!-----------------------------------------------------------------------
      if(lOp.eq.j_int_StartAnalysis)then
!-----------------------------------------------------------------------
!        Create vectors in memory
!-----------------------------------------------------------------------
         ptrC = SMAIntArrayCreate(3,20,0)
         INTCM(1) = kNel
!-----------------------------------------------------------------------
!     Setup of the increment
!-----------------------------------------------------------------------
      elseif(lOp.eq.j_int_SetupIncrement)then
!-----------------------------------------------------------------------
!     Start of the increment
!-----------------------------------------------------------------------
      elseif(lOp.eq.j_int_StartIncrement)then
         ptrC = SMAIntArrayAccess(3)
         INTCM(2) = kInc
         do i=5,20
               INTCM(i) = 0
         enddo
!-----------------------------------------------------------------------
!     End of the increment
!-----------------------------------------------------------------------
      elseif(lOp.eq.j_int_EndIncrement)then
         ptrC = SMAIntArrayAccess(3)
!-----------------------------------------------------------------------
!        Create arrays only when timestep one is finished
!-----------------------------------------------------------------------
         if(kInc.eq.1)then
            INTCM(1) = kNel
!-----------------------------------------------------------------------
!           Arrays coming from VUMAT
!-----------------------------------------------------------------------
            ptrE = SMAFloatArrayCreateDP(5,kNel*7,0.0d0)
            ptrS = SMAFloatArrayCreateDP(6,kNel*7,0.0d0)
!-----------------------------------------------------------------------
!           Arrays send from VEXTERNALDB
!-----------------------------------------------------------------------
            ptrF = SMAFloatArrayCreateDP(7,kNel,0.0d0)
            ptrW = SMAFloatArrayCreateDP(2,kNel,0.0d0)
!-----------------------------------------------------------------------
!        End of the first increment
!-----------------------------------------------------------------------
         else
!-----------------------------------------------------------------------
!        Regular timestep, compute OMEGA and check for fracture
!-----------------------------------------------------------------------
!-----------------------------------------------------------------------
!           Arrays coming from VUMAT
!-----------------------------------------------------------------------
            ptrE = SMAFloatArrayAccess(5)
            ptrS = SMAFloatArrayAccess(6)
!-----------------------------------------------------------------------
!           Arrays send from VEXTERNALDB
!-----------------------------------------------------------------------
            ptrW = SMAFloatArrayAccess(2)
            ptrF = SMAFloatArrayAccess(7)
!-----------------------------------------------------------------------
!           Access number of elements and section points
!-----------------------------------------------------------------------
            nip  = INTCM(3)
            kNel = INTCM(1)
!-----------------------------------------------------------------------
!           Compute bending indicator OMEGA
!-----------------------------------------------------------------------
            do i=1,kNel
               maxeps3 =-1e12
               mineps3 = 1e12
c
               eps3dw  = (eps3(i+kNel*(1-1)))
               eps3up  = (eps3(i+kNel*(nip-1)))
c
               mineps3 = min(eps3dw,eps3up)
               maxeps3 = max(eps3dw,eps3up)
               max_1   = max(abs(eps3dw),abs(eps3up))
c
               if(max_1.ne.0.0)then
                  failureweight(i) = abs((maxeps3-mineps3)/max_1)/2.0
               else
                  failureweight(i) = 0.0
               endif
            enddo
!-----------------------------------------------------------------------
!           Check user-defined number of integration points at fracture
!-----------------------------------------------------------------------
            do i=1,kNel
               if(nip.eq.3)then
                  failstatus = status(i+kNel*(2-1))
               elseif(nip.eq.5)then
                  failstatus = status(i+kNel*(3-1))
               elseif(nip.eq.7)then
                  failstatus = status(i+kNel*(4-1))
               endif
c
               if(failstatus.lt.0.5)then
                  fail(i) = 1
               else
                  fail(i) = 0
               endif
            enddo
         endif
      endif
!-----------------------------------------------------------------------
!     End of the subroutine
!-----------------------------------------------------------------------
   92 FORMAT(1I7,1I7,1E11.4,1I7)
      return
      end