import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useForm } from "react-hook-form"

import { ElectronicDigitalSignaturesService } from "@/client"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { LoadingButton } from "@/components/ui/loading-button"
import useCustomToast from "@/hooks/useCustomToast"
import { handleError } from "@/utils"

interface DeleteElectronicDigitalSignatureProps {
  id: string
  open: boolean
  onOpenChange: (open: boolean) => void
  onSuccess: () => void
}

const DeleteElectronicDigitalSignature = ({
  id,
  open,
  onOpenChange,
  onSuccess,
}: DeleteElectronicDigitalSignatureProps) => {
  const queryClient = useQueryClient()
  const { showSuccessToast, showErrorToast } = useCustomToast()
  const { handleSubmit } = useForm()

  const deleteSignature = async (id: string) => {
    await ElectronicDigitalSignaturesService.digitalSignaturesDeleteElectronicDigitalSignature(
      { path: { id } },
    )
  }

  const mutation = useMutation({
    mutationFn: deleteSignature,
    onSuccess: () => {
      showSuccessToast(
        "The Electronic Digital Signature was deleted successfully",
      )
      onOpenChange(false)
      onSuccess()
    },
    onError: handleError.bind(showErrorToast),
    onSettled: () => {
      queryClient.invalidateQueries({
        queryKey: ["electronic-digital-signatures"],
      })
    },
  })

  const onSubmit = async () => {
    mutation.mutate(id)
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md">
        <form onSubmit={handleSubmit(onSubmit)}>
          <DialogHeader>
            <DialogTitle>Delete Electronic Digital Signature</DialogTitle>
            <DialogDescription>
              This Electronic Digital Signature will be permanently deleted. Are
              you sure? You will not be able to undo this action.
            </DialogDescription>
          </DialogHeader>

          <DialogFooter className="mt-4">
            <DialogClose asChild>
              <Button variant="outline" disabled={mutation.isPending}>
                Cancel
              </Button>
            </DialogClose>
            <LoadingButton
              variant="destructive"
              type="submit"
              loading={mutation.isPending}
            >
              Delete
            </LoadingButton>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}

export default DeleteElectronicDigitalSignature
