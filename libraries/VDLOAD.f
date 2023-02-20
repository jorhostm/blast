      subroutine vdload(
     . nBlock, ndim, stepTime, totalTime,
     . amplitude, curCoords, velocity, dirCos, jltyp, sname,
     . value)
      include 'vaba_param.inc'
      dimension curCoords(nBlock,ndim), velocity(nBlock,ndim),
     . dirCos(nBlock,ndim,ndim),value(nBlock)
      character*80 sname
!-------------------------------------------------------------------------------
      integer i
!-------------------------------------------------------------------------------
!-------------------------------------------------------------------------------
!     Start subroutine
!-------------------------------------------------------------------------------
      do i=1,nBlock
         value(i) = amplitude*dirCos(i,3,3)
      enddo
!-------------------------------------------------------------------------------
!     End of subroutine
!-------------------------------------------------------------------------------
      return
      end
